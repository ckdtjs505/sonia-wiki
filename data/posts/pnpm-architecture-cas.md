---
url: https://ckdtjs505.github.io/posts/pnpm-architecture-cas
layout: post
title: 'pnpm 스토어(CAS)는 파일을 어떻게 저장하고 복원하나: 해시 저장과 하드 링크'
series: 'pnpm 아키텍처'
date: 2026-09-14T12:00:00.000Z
tags: pnpm
comments: true
share: true
related: false
summary: pnpm 글로벌 스토어는 파일을 내용 해시로 한 번만 저장하는 CAS(Content-Addressable Storage)다. 해시 파일명으로 저장된 원본이 설치 때 node_modules/.pnpm에 하드 링크로 복원되는 과정, 하드 링크 파일이 일반 파일처럼 보이는 이유, inode로 직접 확인하는 방법을 정리했다.
---

## 이 글에서 다루는 것

[pnpm node_modules 3계층 구조](/posts/pnpm의-3계층-아키텍처와-링크-메커니즘-분석)의 맨 아래층인 **글로벌 스토어**만 들여다본다. 스토어가 파일을 어떤 이름으로 저장하는지, 설치할 때 그 파일이 어떻게 `node_modules/.pnpm`에 다시 나타나는지, 그리고 그렇게 나타난 파일이 왜 평범한 파일처럼 동작하는지를 다룬다.

## pnpm 스토어는 파일을 어떻게 저장하나요?

pnpm 스토어는 CAS(Content-Addressable Storage), 즉 **파일 이름이 아니라 파일 내용의 해시로 주소를 매기는 저장소**다.

* 패키지를 내려받으면 pnpm은 패키지 안의 파일 하나하나를 해시해서, 그 해시값을 경로로 삼아 스토어의 `files/` 아래에 저장한다. 그래서 스토어 안의 원본 파일은 `a1b2c3d4...`처럼 사람이 읽기 어려운 이름을 가진다.
* 내용이 같은 파일은 해시도 같으므로 한 번만 저장된다. 서로 다른 패키지나 같은 패키지의 다른 버전이 똑같은 파일을 가지고 있어도 디스크에는 한 벌뿐이다.
* 패키지마다 "이 패키지의 `index.js`는 어떤 해시의 파일인가"를 적어 둔 인덱스 정보도 함께 저장한다. 설치할 때 이 인덱스를 보고 원래 파일 이름을 되찾는다.

스토어 위치는 `pnpm store path`로 확인할 수 있다. pnpm 버전에 따라 스토어 디렉터리 이름(`v3`, `v10` 등)과 세부 배치는 다르지만, 내용 해시로 저장하고 인덱스로 복원한다는 원리는 같다.

## 설치할 때 원본은 어떻게 node_modules에 나타나나요?

설치 과정에서 pnpm은 패키지 인덱스를 읽고, 파일마다 스토어의 해시 파일을 `node_modules/.pnpm/<패키지>@<버전>/node_modules/<패키지>/` 아래 원래 이름으로 **하드 링크**한다.

* `~/Library/pnpm/store/.../a1b2c3d4...` (스토어의 해시 이름 원본)
* `node_modules/.pnpm/react@18.2.0/node_modules/react/index.js` (프로젝트에서 보이는 이름)

두 경로는 이름만 다를 뿐 같은 파일이다. 그래서 프로젝트를 여러 개 설치해도 파일 내용만큼의 용량이 반복해서 들지 않는다.

하드 링크는 같은 파일 시스템(같은 디스크 볼륨) 안에서만 만들 수 있다. 스토어와 프로젝트가 다른 디스크에 있으면 pnpm은 하드 링크 대신 복사(또는 파일 시스템이 지원하면 copy-on-write 복제)로 대신한다. 이 동작은 `packageImportMethod`(`.npmrc`에서는 `package-import-method`) 설정으로 바꿀 수 있다.

## 하드 링크된 파일은 왜 일반 파일처럼 보이나요?

하드 링크는 원본과 **같은 inode를 가리키는 또 하나의 디렉터리 엔트리**이기 때문이다. inode는 파일 시스템이 실제 데이터 위치와 권한 같은 정보를 담아 두는 구조체이고, 파일 이름은 그 inode를 가리키는 꼬리표일 뿐이다. 하드 링크를 만들면 꼬리표가 하나 더 생길 뿐 "원본"과 "링크"의 구분이 없다.

그래서 다음처럼 동작한다.

* **편집기:** 파일을 열면 원본 내용이 그대로 보이고 바로 수정할 수 있다.
* **터미널 `ls -l`:** 심볼릭 링크처럼 `->` 화살표가 붙지 않고, 일반 파일(`-rw-r--r--`)로 표시된다. 대신 링크 카운트 숫자가 2 이상으로 올라간다.
* **애플리케이션:** Node.js, Python 같은 런타임은 링크를 따라가는 단계 없이 일반 파일로 바로 읽는다.

반대로 말하면, `node_modules/.pnpm` 안의 파일을 직접 고치면 **스토어 원본도 같이 바뀐다.** 같은 패키지를 쓰는 다른 프로젝트에도 그 수정이 보이므로, 패키지를 고쳐야 한다면 `pnpm patch`처럼 정식 경로를 쓰는 편이 안전하다.

## 직접 확인하려면?

pnpm 없이도 하드 링크의 성질은 터미널에서 바로 확인할 수 있다. 해시 이름의 원본 파일에 사람이 읽기 쉬운 이름으로 하드 링크를 하나 걸어 본다.

```bash
# 1. 하드 링크 생성 (스토어 원본 → 읽기 쉬운 이름)
ln ~/cas-store/a1b2c3d4e5f6 ~/my-notes/오늘할일.txt

# 2. inode와 링크 카운트 확인
ls -li ~/cas-store/a1b2c3d4e5f6 ~/my-notes/오늘할일.txt
# 출력: 두 줄의 맨 앞 inode 번호가 같고, 링크 카운트가 2로 표시된다
# 12345678 -rw-r--r-- 2 user group ... a1b2c3d4e5f6
# 12345678 -rw-r--r-- 2 user group ... 오늘할일.txt
```

Node.js에서도 링크라는 걸 신경 쓸 필요 없이 일반 파일처럼 읽힌다.

```javascript
const fs = require('fs');
const os = require('os');
const path = require('path');

// 일반 파일과 완전히 동일한 방식으로 처리
// Node.js는 셸과 달리 `~`를 홈 디렉터리로 바꿔 주지 않으므로 os.homedir()로 경로를 만듦
const content = fs.readFileSync(path.join(os.homedir(), 'my-notes', '오늘할일.txt'), 'utf-8');
console.log(content);
```

실제 pnpm 프로젝트에서는 `node_modules/.pnpm/<패키지>@<버전>/node_modules/<패키지>/` 안의 파일에 `ls -li`를 해 보면 링크 카운트가 2 이상인 것을 볼 수 있다.

## 느낀점

CAS 저장소는 해시 파일명 덕분에 중복 제거와 무결성 확인이 쉽지만, 그대로는 사람이 쓰기 어렵다. pnpm은 하드 링크로 "해시 이름의 원본"과 "익숙한 경로의 파일"을 같은 파일로 만들어서, 저장은 CAS로 하고 사용은 평범한 `node_modules`처럼 하게 했다.

## 결론

pnpm 스토어는 파일을 내용 해시로 한 번만 저장하고, 설치할 때 인덱스를 보고 원래 이름으로 하드 링크해서 복원한다. 하드 링크는 같은 inode를 공유하는 또 하나의 이름이라 일반 파일처럼 읽히고, 파일 내용만큼의 디스크 용량이 반복해서 들지 않는다.

## 참고

- [pnpm node_modules 구조: 글로벌 스토어·가상 스토어·심볼릭 링크 3계층](/posts/pnpm의-3계층-아키텍처와-링크-메커니즘-분석)
- [pnpm 공식 문서: 동기 (콘텐츠 주소 지정 저장소)](https://pnpm.io/ko/motivation)
- [pnpm 공식 문서: 심볼릭 링크된 node_modules 구조](https://pnpm.io/ko/symlinked-node-modules-structure)
- [pnpm 공식 문서: packageImportMethod 설정](https://pnpm.io/ko/settings#packageimportmethod)
