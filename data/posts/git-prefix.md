---
url: https://ckdtjs505.github.io/posts/git-prefix
layout: post
title: 'Git 브랜치 네이밍 컨벤션과 `feature/` 접두사의 역할'
date: 2026-09-14T00:00:00.000Z
tags: Git
comments: true
share: true
related: false
summary: Git 브랜치 이름의 feature/는 새 기능 개발 브랜치임을 나타내는 관례적 접두사다. fix/·hotfix/·refactor/·chore/ 같은 접두사의 의미, 슬래시로 나누면 좋은 이유(GUI 폴더 묶음, CI 조건 분기), 작업자·티켓 번호를 붙인 네이밍 예시를 정리했다.
---

## 이 글에서 다루는 것
* 브랜치 이름 앞에 `feature/` 같은 접두사를 붙이는 이유와 효과
* 협업과 CI/CD 파이프라인에서 브랜치를 알아보기 쉽게 관리하는 네이밍 규칙

## Git 브랜치의 `feature/` 접두사는 무엇인가요?
`feature/`는 **새 기능을 개발하는 브랜치**임을 나타내는 관례적 접두사로, Git Flow와 Atlassian의 Feature Branch Workflow에서 널리 쓰인다. Git 자체가 강제하는 규칙은 아니고 팀이 정하는 약속이다.

* 슬래시(`/`)로 나누면 VS Code, Sourcetree 같은 GUI 도구에서 브랜치가 폴더 트리처럼 묶여 보인다.
* `작업자/작업종류/이슈티켓-작업내용` 구조로 쓰면 누가 무엇을 왜 하는지 브랜치 이름만 보고 알 수 있다.

## 브랜치 이름에 접두사를 붙이면 뭐가 좋나요?
커밋을 열어 보기 전에 작업 의도를 알 수 있고, 자동화 조건으로도 쓸 수 있다.

* **작업 성격을 바로 알 수 있다**: 기능 개발인지 버그 수정인지 문서 작업인지 커밋 이력을 보기 전에 파악할 수 있다.
* **CI/CD 조건 분기에 쓸 수 있다**: `release/*`, `hotfix/*` 같은 패턴으로 테스트·빌드·배포 파이프라인을 나눌 수 있다.
* **GUI 도구에서 정리돼 보인다**: 브랜치가 많아져도 계층형 트리로 묶여서 찾기 쉽다.

## 자주 쓰는 브랜치 접두사에는 무엇이 있나요?
* `feature/`: 새로운 기능 개발
* `bugfix/` 또는 `fix/`: 일반적인 버그와 결함 수정
* `hotfix/`: 운영 환경(Production)에서 급하게 고쳐야 하는 오류 패치
* `refactor/`: 동작은 그대로 두고 코드 구조를 개선하거나 최적화
* `chore/`: 빌드 스크립트, 의존성 패키지 관리, 기타 단순 설정 변경

## 실제로는 어떻게 쓰나요?
* 신규 기능 브랜치 생성 및 전환:
  ```bash
  git checkout -b ckdtjs505/feature/PROJ-101-chat-packet-pipeline
  ```
* 긴급 핫픽스 브랜치 생성:
  ```bash
  git checkout -b hotfix/PROJ-102-memory-leak-fix
  ```
* 특정 작업자나 접두사의 브랜치만 골라 보기:
  ```bash
  git branch --list "ckdtjs505/*"
  ```

## 느낀점
* 브랜치 이름만 보고도 PR(Pull Request) 리뷰 전에 작업 범위를 예상할 수 있어 커뮤니케이션 비용이 줄었다.
* 작업자와 티켓 번호를 붙인 계층형 이름이 큰 프로젝트에서 브랜치 충돌과 혼선을 줄여 준다.

## 결론
* 브랜치 네이밍 컨벤션은 단순한 작명 규칙이 아니라 협업 효율, 형상 관리 시각화, 자동화 파이프라인의 기반이다.

## 참고
* [Atlassian: Git Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
* [Atlassian: Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
* [GitHub Docs: GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)

## 요약 이미지
```text
[Repository]
├── ckdtjs505/
│   └── feature/
│       └── PROJ-101-chat-packet-pipeline  ──> (신규 기능 개발)
├── hotfix/
│   └── PROJ-102-memory-leak-fix           ──> (운영 긴급 조치)
└── release/
    └── v1.2.0                               ──> (배포 파이프라인 연동)
```