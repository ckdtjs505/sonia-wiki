---
url: https://ckdtjs505.github.io/posts/2020-07-27-Skill-JS-Array
layout: post
title: '[JS] 코딩 기술 배열(Array)편'
date: 2020-07-27T00:00:00.000Z
tags: javascript skill-Js
comments: true
share: true
related: false
summary: 자바스크립트 배열(Array)의 기초적인 다루는 방법과 유용한 내장 메서드들을 살펴봅니다.
---

데이터 컬렉션은 어떻게 관리하는게 효율적일까?

js에서 제공하는 데이터 컬렉션은 `배열`, `객체`, `Map`, `Set`, `WeakMap`, `WeakSet`가 있다.

그중 가장 조작이 간편한 데이터 컬렉션은 `배열`이다. 뿐 아니라 놀라울 정도로 유연성을 가지고 있다. 그래서 많은 경우 `배열`을 사용하여 데이터를 다루게 된다. 

먼저 배열에서 많이 사용되는 상황을 생각해보자. 
1. 배열에 특정값이 있는지 확인하기. 
2. 배열에 특정 값을 제거하기. 

### 배열에 특정값이 있는지 확인하기
이모티콘 리스트가 있다. 동일한 이모티콘이 있으면 추가하지 않아야한다. 이런 경우 동일한 이모티콘이 있는지 확인해야한다. 과거 ES6이전에는 indexOf 메서드는 값이 없는 경우 -1을 리턴하는 방식으로 구현했다. 
```js
var emoticonList = [ "cap", "love", "game", "man"];
function isEmoticon (emoticonList, value){
    if(emoticonList.indexOf(value) > -1 )
        return true;
    return false;
}
isEmoticon( emoticonList, "cap");       //true
isEmoticon( emoticonList, "cep");       //false
```
최근 ES6 자바스크립트에서는 includes라는 true, false를 반환하는 메서드를 제공하고 있다. 앞서 만든 코드를 리펙토링 해보자. 

```js
const emoticonList = [ "cap", "love", "game", "man"];
emoticonList.includes("cap");           //true
emoticonList.includes("cep");           //false
``` 
위와같은 방식으로 훨씬 더 간결하게 값의 존재여부를 확인할 수 있다. 많이 사용하자 ㅎㅎ 

### 배열에 특정 값 제거하기 
[ 1, 2, 3, 4, 5] 배열에서 숫자 3을 제거하는 코드를 만들어보자. 간단하게 로직을 짜면 배열에 숫자 3의 위치를 찾고 그 값을 제거한다. 

```js
const arr = [ 1, 2, 3, 4, 5 ];
function removeItem(arr, val) {
    const itemIdx = arr.indexOf(val);
    arr.splice(itemIdx, 1);
    return arr;
}

removeItem(arr, 2);                 // [1, 3, 4, 5]
console.log(arr);                   // [1, 3, 4, 5]
```

위에 있는 코드는 좋은 코드일까? 간결해보이기는 하지만 치명적인 오류를 가져올수 있는 코드이다. 왜냐하면 원본이 수정되기 때문이다. 절대 원본을 조작해서는 안된다. 알게 모르게 사이드 이펙트가 생길 수 있다. 원본이 수정되지 않는 코드를 작성해보자 

```js
const arr = [ 1, 2, 3, 4, 5 ];
function removeItem(arr, val) {
    const itemIdx = arr.indexOf(val);
    return [ ...arr.slice(0, itemIdx), ...arr.slice(itemIdx + 1)];
}

removeItem(arr, 2);                 // [1, 3, 4, 5]
console.log(arr);                   // [1, 2, 3, 4, 5]
```

오늘 배운 내용을 간단하게 정리해보자 
데이터 컬랙션으로 배열을 배웠다. 
첫째로 배열에 존재하는 값을 찾기위한 includes 메서드를 알았다. 
둘째로 배열의 조작을 피하는 방법으로 펼침 연산자에 대해 알았다.

배열의 조작이 그렇게 큰 이슈인가 생각했는데, 예시로 조작의 문제점을 직접 느껴보니 조작이 생각보다 큰 이슈임을 알 수 있었다.
배열이 조작되지 않도록 프로그래밍 하도록 하자 
