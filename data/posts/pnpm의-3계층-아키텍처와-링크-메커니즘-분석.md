---
url: https://ckdtjs505.github.io/posts/pnpm%EC%9D%98-3%EA%B3%84%EC%B8%B5-%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%EC%99%80-%EB%A7%81%ED%81%AC-%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98-%EB%B6%84%EC%84%9D
layout: post
title: 'pnpm node_modules 구조: 글로벌 스토어·가상 스토어·심볼릭 링크 3계층과 유령 의존성 차단'
series: 'pnpm 아키텍처'
date: 2026-09-14T00:00:00.000Z
tags: pnpm
comments: true
share: true
related: false
summary: pnpm은 글로벌 스토어(원본 1벌), 가상 스토어(node_modules/.pnpm, 하드 링크), 앱 node_modules(심볼릭 링크) 3계층으로 디스크 중복을 없애고, package.json에 적은 의존성만 보이게 해 유령 의존성을 막는다. 각 계층이 하는 일과 확인 방법을 정리했다.
---

## 이 글에서 다루는 것

pnpm이 **Global Store**, **Virtual Store(`.pnpm`)**, **개별 앱의 `node_modules`** 세 계층을 어떻게 연결해서 디스크 공간을 아끼고 유령 의존성(phantom dependency)을 막는지 정리한다. 글로벌 스토어 안에서 파일이 어떻게 저장되고 하드 링크로 복원되는지는 이어지는 글 [pnpm 스토어(CAS)는 파일을 어떻게 저장하고 복원하나](/posts/pnpm-architecture-cas)에서 다룬다.

## pnpm의 node_modules는 어떤 구조인가요?

pnpm은 패키지 파일을 세 단계로 나눠 둔다.

* **1단계, 글로벌 스토어:** 실제 파일 원본이 컴퓨터 전체에서 딱 한 벌만 저장되는 곳이다. 파일 내용의 해시로 주소를 매기는 CAS(Content-Addressable Storage) 방식이다. macOS 기준 위치는 `~/Library/pnpm/store`다.
* **2단계, 가상 스토어:** 프로젝트 안의 `node_modules/.pnpm`이다. 패키지마다 `react@18.2.0` 같은 폴더가 평탄하게 놓이고, 그 안의 파일은 글로벌 스토어 원본을 가리키는 하드 링크다. 같은 디스크 블록을 공유하므로 파일 내용만큼 용량이 더 들지 않는다.
* **3단계, 앱의 node_modules:** `apps/*/node_modules`에는 실제 파일 없이 가상 스토어를 가리키는 심볼릭 링크만 놓인다. 그래서 각 앱은 자기 `package.json`에 적은 패키지만 볼 수 있다.

```text
[1] Global Content Store (원본 1벌 저장)
    ~/Library/pnpm/store
              │
              │ 하드 링크: 같은 inode 공유, 데이터 블록 추가 없음
              ▼
[2] Project Virtual Store
    my-monorepo/node_modules/.pnpm/react@18.2.0/node_modules/react
              │
              │ 심볼릭 링크: 경로 바로가기
              ▼
[3] Apps / Packages (프로젝트가 실제로 require하는 위치)
    ├── apps/web/node_modules/react
    └── apps/tv/node_modules/react
```

## 왜 하드 링크와 심볼릭 링크를 섞어 쓰나요?

두 링크가 맡는 일이 다르기 때문이다.

* **하드 링크(1단계 → 2단계)는 디스크 중복을 없앤다.** 하드 링크는 원본과 같은 inode를 가리키는 또 하나의 파일 이름이라, 프로젝트가 10개여도 `react`의 파일 내용은 디스크에 한 번만 저장된다. Node.js 입장에서는 링크 흔적이 없는 일반 파일이라 별도 처리 없이 읽힌다.
* **심볼릭 링크(2단계 → 3단계)는 의존성 경계를 만든다.** 앱의 `node_modules` 최상위에는 `package.json`에 적은 패키지의 심볼릭 링크만 놓인다. npm처럼 하위 의존성까지 최상위로 끌어올리는(호이스팅) 구조가 아니라서, 적지 않은 패키지를 `require`하면 바로 에러가 난다.

## 유령 의존성은 어떻게 막히나요?

유령 의존성은 `package.json`에 적지 않았는데 다른 패키지의 하위 의존성이 최상위로 호이스팅돼서 우연히 `require`되는 패키지를 말한다. 그 하위 의존성이 버전업되거나 빠지면 아무 변경도 안 한 내 코드가 깨진다.

pnpm에서는 앱의 `node_modules`에 내가 적은 패키지의 링크만 있다. 하위 의존성은 `.pnpm/<패키지>@<버전>/node_modules` 안에서 그 패키지끼리만 보이도록 링크된다. 그래서 적지 않은 패키지에 접근하면 설치 시점이 아니라 개발 중에 바로 실패해서, 문제를 일찍 발견할 수 있다.

## 내 프로젝트에서 직접 확인하려면?

심볼릭 링크는 `ls -l`로 바로 보인다.

```bash
# 앱의 react가 가상 스토어를 가리키는 심볼릭 링크인지 확인
ls -l apps/web/node_modules/react
# 결과 예: react -> ../../../node_modules/.pnpm/react@18.2.0/node_modules/react
```

가상 스토어의 파일이 글로벌 스토어 원본과 같은 inode를 쓰는지(하드 링크인지)는 [다음 글의 inode 확인 예시](/posts/pnpm-architecture-cas)에서 직접 따라 해 볼 수 있다.

## 느낀점

* "빠르고 가볍다"는 장점은 결과일 뿐이고, 그 바탕은 파일 시스템의 하드 링크와 심볼릭 링크를 역할별로 나눠 쓴 설계라는 점이 인상적이었다.
* npm의 호이스팅에서 생기는 런타임 버그와 모노레포의 중복 설치 문제를 패키지 매니저 규칙이 아니라 디렉터리 구조로 풀었다.

## 결론

pnpm은 **원본 1벌 저장(글로벌 스토어) → 하드 링크로 펼치기(.pnpm) → 심볼릭 링크로 노출(앱 node_modules)** 순서로 디스크 사용량을 줄이고, 적은 의존성만 보이게 해서 유령 의존성을 막는다.

## 참고

* [pnpm 공식 문서: 심볼릭 링크된 node_modules 구조](https://pnpm.io/ko/symlinked-node-modules-structure)
* [pnpm 공식 문서: 동기 (디스크 공간 절약과 엄격한 node_modules)](https://pnpm.io/ko/motivation)
* [pnpm 스토어(CAS)는 파일을 어떻게 저장하고 복원하나](/posts/pnpm-architecture-cas)
