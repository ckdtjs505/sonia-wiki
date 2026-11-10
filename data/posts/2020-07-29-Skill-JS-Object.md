---
url: https://ckdtjs505.github.io/posts/2020-07-29-Skill-JS-Object
layout: post
title: '[JS] 코딩 기술 객체(object)편'
date: 2020-07-29T00:00:00.000Z
tags: javascript skill-Js
comments: true
share: true
related: false
summary: '자바스크립트 객체(Object)의 생성, 속성 접근, 순회 방법 등 객체 다루기의 기본을 익힙니다.'
---

## 목표 
* js 데이터 컬랙션 객체(object)을 이해한다.
* js 데이터 컬랙션 객체(object)의 역할을 이해한다. 
* js 데이터 컬랙션 객체(object)의 사용법을 익힌다.
* js 데이터 컬랙션 객체(object)를 사용한 예제를 익힌다. 

## 객체(object)의 개념 요약

* 객체는 자바스크립트를 이루는 거의 모든 것이다.
  * 함수(function), 배열(Array), 정규 표현식(RegExp), Date 모두 객체이다. 
  * 원시 타입 제외 ( String, Number, Boolean, null, undefined )
* 객체는 키(key)와 값(value)로 구성된 프로퍼티(Property)들의 집합이다.
* 객체는 프로토타입(prototype)을 이용해 다른 객체의 프로퍼티와 메소드를 상속 받을 수 있다.

## 객체(object)의 구체적인 개념 
* 객체 리터럴을 이용해 객체 생성하기 
```
let person = {
 name : "changsun",
 gender : "male"
}
console.log(type person);   // object
```
* person 객체는 2개의 프로퍼티가 존재(name, gender)
* name 프로퍼티는 key가 "name"이고 value가 "changsun"
* gender 프로퍼티는 key가 "gender"이고 value "male"

## 객체(object)의 사용 예제 
* 객체가 가장 많이 사용되는 경우는 API응답값으로 많이 사용된다.
* 객체의 갱신 - object.assign 메서드. 
```js
const smallEmoticon = {
    "/하이/" : { title : "하이" }
    "/빡침/" : { title : "빡침" }
}
const bigEmoticon = {
    "/하이염/" : { title : "하이염" }
}
// 이모티콘이 합쳐진다
const allEmoticon = Object.assign( {}, smallEmoticon, bigEmoticon); 
```

