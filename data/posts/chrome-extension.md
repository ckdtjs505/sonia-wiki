---
url: https://ckdtjs505.github.io/posts/chrome-extension
layout: post
series: '임베디드 브라우저'
title: 'Chrome 확장 프로그램: VOD 데이터 패킷 대량 주입 파이프라인 분석'
featured: true
date: 2026-09-09T23:21:40.707Z
tags: [Chrome Extension, Web Worker]
comments: true
share: true
related: false
summary: VOD 플레이어 내부 큐에 가상 데이터 패킷 10,000개를 한 번에 주입하는 Chrome 확장 프로그램을 만들며 정리한 5단계 격리 컨텍스트 통신 구조와 Web Worker·타임 오프셋 치환 방식
---

## 이 글에서 다루는 것

* Chrome 확장 프로그램의 5단계 레이어 통신 구조를 파악하고, Web Worker와 타임 오프셋 치환 방식을 활용해 VOD 플레이어 내부 큐에 10,000개의 가상 데이터 패킷을 효율적으로 주입하는 흐름을 정립합니다.

## VOD 플레이어에 패킷 10,000개를 어떻게 한 번에 넣나요?

Web Worker에서 10,000개를 XML 문자열 하나로 미리 만들어 **한 번의 `postMessage`로 넘기고**, 시간 값은 자리표시자로 두었다가 페이지에 넣는 순간 현재 재생 시간 기준으로 바꿔 넣습니다.

* **VOD vs LIVE 모드 파라미터 차이:** VOD 모드에서 `rate`는 초당 전송률이 아니라 **총 생성 패킷 수**를 의미합니다.
* **단일 벌크 전송 (Bulk Transfer):** 1초마다 tick 단위로 패킷을 발행하는 LIVE 모드와 달리, START 시점에 Web Worker에서 10,000개 패킷 전체를 단일 `<root>` XML 문자열로 일괄 생성해 단 1회의 `postMessage`로 전달합니다.
* **타임 오프셋 플레이스홀더 패턴:** 생성 시점에는 `__VOD_TIME_OFFSET_{s}__` 형태로 상대 시간(초)을 마킹하고, 최종 주입 계층(`page.js`)에서 실제 `videoEl.currentTime + 2초`를 기준으로 절대 타임스탬프로 일괄 치환합니다.
* **5단계 격리 컨텍스트 통신:** `Popup UI (popup.js)` → `Content Script (content.js)` → `Web Worker (worker.js)` → `Content Script (content.js)` → `Page Script (page.js)` → `VOD Player` 순으로 데이터를 중계합니다.

## 확장 프로그램은 왜 페이지의 JS 변수에 바로 접근하지 못하나요?

Chrome 확장 프로그램의 content script는 웹 페이지와 DOM은 공유하지만, **JavaScript 실행 환경은 분리된 별도의 세계(isolated world)에서 돌아갑니다.** 그래서 content script에서는 페이지가 만든 전역 변수나 플레이어 객체(`dataItem` 같은)에 직접 손댈 수 없습니다.

페이지의 객체를 다뤄야 할 때는 페이지 컨텍스트에서 실행되는 스크립트(page script)를 따로 넣고, 둘 사이를 `window.postMessage`로 잇는 방식이 일반적입니다. 이 글의 파이프라인이 5단계로 길어진 것도 이 경계 때문입니다.

| 컨텍스트 | 페이지 DOM | 페이지 JS 변수 | chrome.* API | 서로 통신하는 방법 |
|---|---|---|---|---|
| Popup (`popup.js`) | X | X | O | `chrome.tabs.sendMessage` |
| Content Script (`content.js`) | O | X | 일부 | `chrome.runtime` 메시지, `window.postMessage` |
| Page Script (`page.js`) | O | O | X | `window.postMessage` |
| Web Worker (`worker.js`) | X | X | X | `worker.postMessage` |

## 데이터는 어떤 단계를 거쳐 플레이어에 도착하나요?

전체 파이프라인은 Chrome 확장 프로그램의 보안 격리 환경을 넘나드는 5단계 레이어로 구성됩니다.

```text
[클릭] startBtn (popup.js)
   │ chrome.tabs.sendMessage → { type: 'START', rate: 10000, durationMs: 60000, mode: 'vod' }
   ▼
[content.js] → worker.postMessage('START')
   │
   ▼
[worker.js] ── vodpackets.js 10,000회 호출 ──▶ bigXml (<root>..10000개..</root>)
   │ self.postMessage({ type: 'VOD_BULK', xmlString: bigXml })
   ▼
[content.js] → window.postMessage('VOD_TESTER_PACKET')
   │
   ▼
[page.js] ── DOMParser로 XML 파싱
           ── __VOD_TIME_OFFSET_N__ → 실제 재생시간 + N으로 치환
           ── dataItem.createData() × 10,000
           ── dataItem.queue.push() × 10,000
   │
   ▼
[VOD 플레이어] 재생 시간 도달 시 데이터 자동 렌더링

```

### 1단계: Popup UI — 버튼 클릭 (`popup.js`)

사용자로부터 총 패킷 수(`rate`)와 분배 구간(`durationMs`)을 입력받아 `content.js`로 전달합니다.

```javascript
// popup.js L434-442
startBtn.onclick = async () => {
  const rate = Math.max(1, Number(rateInput.value) || 1); // 예: 10000
  const durationMs = Number(durationSelect.value) || 0;   // 예: 60000 (1분)
  const r = await send({ type: 'START', rate, durationMs, mode: 'vod' });
  applyStatus(r);
};

```

### 2단계: Worker — 10,000개 XML 패킷 일괄 생성 (`worker.js`)

메인 스레드 부하를 방지하기 위해 Web Worker 내부에서 타임 오프셋을 균등 분배한 후 단일 `<root>` XML 덩어리로 합산합니다.

```javascript
// worker.js L157-184
case 'START': {
  if (mode === 'vod') {
    const durationSec = Math.floor(dur / 1000);  // 예: 60초
    const totalPackets = rate;                    // 10,000개

    let bigXml = '<root>';
    for (let i = 0; i < totalPackets; i++) {
      // 0~59초 구간에 균등 분배 (i=0 → 0초, i=9999 → ~59초)
      const s = Math.floor((i / totalPackets) * durationSec);
      const k = pickKey();           // 가중치 추첨 (데이터 95%)
      let xml = entry.fn().xmlString; // vodpackets.js 에서 XML 생성
      xml = xml.replace('__VOD_TIME__', `__VOD_TIME_OFFSET_${s}__`);
      bigXml += xml;
    }
    bigXml += '</root>';

    // 단 한 번의 메시지로 전체 묶음 전송
    self.postMessage({ type: 'VOD_BULK', xmlString: bigXml, count });
  }
}

```

### 3단계: 개별 XML 패킷 생성 (`vodpackets.js`)

개별 패킷은 시간 치환용 플레이스홀더(`__VOD_TIME__`)를 포함하는 템플릿 형태로 반환됩니다.

```javascript
// vodpackets.js
export function vodChat() {
  return {
    tagName: 'data',
    xmlString: '<data><p>0</p><n><![CDATA[User1]]></n><u>tester1</u><m><![CDATA[Test Message]]></m><t>__VOD_TIME__</t></data>',
  };
}

```

### 4단계: Content Script — 메인 페이지 컨텍스트 전달 (`content.js`)

Worker로부터 수신한 대량 XML 데이터를 메인 웹 페이지 스크립트 실행 컨텍스트로 중계합니다.

```javascript
// content.js
window.postMessage({ type: 'VOD_TESTER_PACKET', xmlString: bigXml }, '*');

```

### 5단계: Page Script — 타임 치환 및 플레이어 큐 적재 (`page.js`)

현재 비디오 재생 위치(`videoEl.currentTime + 2초`)를 기준으로 오프셋을 절대 시간으로 일괄 치환한 후, 파싱한 데이터를 VOD 플레이어 내부 큐에 직접 적재합니다.

```javascript
// page.js L104-160
// 현재 재생 시간 기준으로 오프셋 변환
const currentTime = videoEl.currentTime;
const time = currentTime + 2; // 현재 재생 위치 + 2초 앞

// __VOD_TIME_OFFSET_3__ → String(currentTime + 2 + 3)
replacedXmlString = d.xmlString.replace(
  /__VOD_TIME_OFFSET_(\d+)__/g,
  (_, offset) => String(time + Number(offset))
);

// XML 파싱 후 chatItem에 삽입
const xmlDoc = vodParser.parseFromString(replacedXmlString, 'text/xml');
const children = Array.from(xmlDoc.documentElement.children); // 10,000개 노드
for (const child of children) {
  const parsedData = dataItem.createData(child); // 내부 파싱 함수
  if (parsedData) dataItem.queue.push(parsedData);     // 플레이어 내부 데이터 큐에 삽입
}

```

### 모드별 아키텍처 비교

<style>
  .custom-table { border-collapse: collapse; width: 100%; margin-bottom: 20px; font-size: 0.95em; }
  .custom-table th, .custom-table td { border: 1px solid #d0d7de; padding: 12px 15px; }
  .custom-table th { background: linear-gradient(135deg, #4e54c8, #8f94fb); color: #fff; font-weight: 600; text-align: center; border-bottom: 2px solid #d0d7de; }
  .custom-table td { text-align: left; }
</style>
<table class="custom-table">
  <thead>
    <tr>
      <th>구분</th>
      <th>LIVE 모드</th>
      <th>VOD 모드</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>패킷 생성 시점</strong></td>
      <td>1초마다 주기적 tick 발생</td>
      <td>START 시점 1회 일괄(Bulk) 생성</td>
    </tr>
    <tr>
      <td><strong>rate의 의미</strong></td>
      <td>초당 전송 패킷 수</td>
      <td>총 주입 패킷 수 (예: 10,000개)</td>
    </tr>
    <tr>
      <td><strong>주입 방식</strong></td>
      <td><code>ctrl.receive()</code> (소켓 실시간 소비)</td>
      <td><code>dataItem.queue.push()</code> (플레이어 큐 사전 적재)</td>
    </tr>
    <tr>
      <td><strong>시간 처리</strong></td>
      <td>별도 타임스탬프 계산 불필요</td>
      <td>현재 재생 시간 + 상대 오프셋 치환</td>
    </tr>
    <tr>
      <td><strong>tick 루프 역할</strong></td>
      <td>패킷 생성 및 지속 전송</td>
      <td>UI 메트릭 측정 상태 유지만 수행</td>
    </tr>
  </tbody>
</table>

## 느낀점

* 대용량 문자열 결합 및 10,000회 루프 처리를 Web Worker로 격리하여 팝업과 브라우저 메인 스레드의 프리징 현상을 방지한 구조가 인상적입니다.
* 실시간 스트림과 달리 타임라인 기반으로 동작하는 VOD 특성에 맞춰, 생성 시점에는 상대 오프셋으로 기록하고 주입 시점에 실제 비디오 재생 시간과 결합하는 '오프셋 치환 패턴'을 통해 재생 오차를 효과적으로 해결했습니다.

## ToDo

* 10,000개 노드를 `DOMParser`로 일괄 파싱하고 순회할 때 메인 스레드 프레임 드랍(Long Task) 발생 여부 프로파일링.
* 한 번에 10,000개를 밀어 넣는 방식 대신 `requestAnimationFrame` 또는 청크 단위(예: 1,000개씩 분할) 큐 삽입 적용 검토.
* 사용자가 VOD 재생바를 탐색(Seek)하거나 되감기/빨리감기를 했을 때 기존 주입된 가상 데이터 큐의 지속/초기화 동작 검증.

## 결론

* VOD 환경의 대량 부하 테스트는 실시간 소켓 주입 방식이 아닌 **사전 일괄 생성 후 플레이어 내부 타임라인 큐 적재 방식**을 취합니다.
* 5단계 레이어를 거치며 연산 부하(Worker), 브릿지 중계(Content Script), 도메인 로직 주입(`page.js`)의 책임을 명확히 분리하여 브라우저 부담을 최소화하면서 대규모 VOD 데이터 렌더링을 구현할 수 있습니다.