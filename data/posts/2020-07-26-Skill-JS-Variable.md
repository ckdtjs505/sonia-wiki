---
url: https://ckdtjs505.github.io/posts/2020-07-26-Skill-JS-Variable
layout: post
title: '[JS] 코딩 기술 변수 선언편'
date: 2020-07-26T00:00:00.000Z
tags: javascript skill-Js
comments: true
share: true
related: false
summary: '자바스크립트 변수 선언 방식(var, let, const)의 차이점과 호이스팅 현상을 정리합니다.'
---

어떻게 하면 사이드 이펙트를 최소화 할 수 있을까? 

첫번째 변수 할당 
변수 할당하는 방법으로 `var`, `const`, `let`이 있다. 결론부터 말하면 `const` => `let` => `var` 순으로 사용하자.
`const`는 재할당이 불가능하다. 이에 반에 `let`은 재할당이 가능하며 `var`는 ES5 이하 에서도 동작한다. 
오른쪽으로 가면 갈수록 자유도가 높아진다. 자유도가 높아질수록 변수의 의미를 파악하기 힘들고, 생각지도 못한 오류에 직면하게 된다. 

간단하게 `const`는 재할당이 불가능하며, `let`은 재할당이 가능하며, `var`는 재할당이 가능하지만 스코프의 범위가 함수로 지정된다. 
각각에 대하여 조금 구체적으로 알고 싶으면 구글에 찾아보자 ㅎㅎ
