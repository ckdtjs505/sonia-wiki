---
url: https://ckdtjs505.github.io/posts/2020-05-08-Core-JS-lexicalEnvironment
layout: post
title: '[Core JS] 렉시컬 환경이란?'
series: 'Core JS'
date: 2020-05-08T00:00:00.000Z
author: changsun oh
tags: javascript CoreJS
comments: true
share: true
related: false
summary: 렉시컬 환경(Lexical Environment)과 스코프 체인의 동작 원리를 상세히 분석합니다.
---

```javascript
var name = 'global';
var log = function () {
  console.log(name);
}

var outer = function() {
  name = 'outer';
  log();
}
outer();

// 실행결과 
// outer
```

1. 전역 컨텍스트 생성  
  `LexicalEnvironment`  
   environmentRecord : { name : 'global', log : f, outer : f}
   outerEnvironment : {}
   
2. outer 컨텍스트 생성   
  `LexicalEnvironment`  
   environmentRecord : {}
   outerEnvironment : { name : 'global' -> 'outer', log : f, outer : f }

3. log 컨텍스트 생성  
   `LexicalEnvironment`  
   environmentRecord : {}
   outerEnvironment : { name : 'global' -> 'outer', log : f, outer : f }



위 코드를 약간만 수정해보자. 

어휘적 환경 

```javascript
var name = 'global';
var log = function () {
  console.log(name);
}

var outer = function() {
  var name = 'outer';
  log();
}
outer();
```

1. 전역 컨텍스트 생성
  `LexicalEnvironment`
   environmentRecord : { name : 'global', log : f, outer : f}
   outerEnvironment : {}
   
2. outer 컨텍스트 생성 
  `LexicalEnvironment`
   environmentRecord : { name : 'outer' }
   outerEnvironment : { name : 'global', log : f, outer : f}

3. log 컨텍스트 생성 
   `LexicalEnvironment`
   environmentRecord : {}
   outerEnvironment : { name : 'global', log : f, outer : f}

log 컨텍스트에서 name은 'global'이므로 global을 출력하게 된다. 
이러한 현상으로 `스코프가 함수가 호출할 때가 아니라 선언할 때` 생긴다고 말씀하시는 분들도 있지만, 그것보다는 실행 컨텍스트가 어떻게 동작하는지 이해하고 접근한다면 훨씬 도움이 될꺼라 믿습니다. 




```javascript
function outer() {
  var a = 0;
  function inner(){
    console.log(++a);
  }
  return inner();
}
outer(); 
outer();

/*
  실행결과 
  1
  1 
*/

```
1. 8번째줄 outer 함수를 실행하면서 변수 a에 0을 할당한다 
2. 이후 inner 함수에서 outer 함수 변수 a에 접근하여 1을 증가한값인 1을 출력한다.
3. 9번째줄 또한 outer 함수를 새로 실행하면서 변수 a에 0을 할당한다.
이후 동일하게 inner 함수에서 outer 함수 변수 a에 접근하여 1을 증가한값인 1을 출력한다. 

outer 함수가 종료된 이후에 inner함수를 호출할수 없는 코드이다. 
어찌보면 너무 당연한 말이지만, 이런경우도 있을수 있다. 
어떤경우에는 outer 함수가 종료된 이후에도 inner 함수를 호출 할 수 있다.
코드로 살펴보자.

> 함수가 종료된 뒤에도 내부 함수가 바깥 변수에 접근하는 경우는 [[Core JS] 클로저란?](/posts/2020-05-06-Core-JS-Closure)에서 코드로 이어서 다룹니다.
