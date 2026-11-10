---
url: https://ckdtjs505.github.io/posts/2020-08-01-Skill-JS-Map
layout: post
title: '[JS] 코딩 기술 맵(map)편'
date: 2020-08-01T00:00:00.000Z
tags: javascript skill-Js
comments: true
share: true
related: false
summary: ES6에서 추가된 Map 객체의 특징과 일반 Object와의 차이점을 분석합니다.
---

## 목표 
* js 데이터 컬랙션 맵(map)의 등장 배경을 이해한다.
* js 데이터 컬랙션 맵(map)을 이해한다.

## 맵의 등장 배경 
* 객체만 봐서는 어떤 의도를 가지고 만들었는지 명확하지 않다.

## 맵의 개념 요약 
* key - value 로 이루어진 컬렉션
* key를 사용해 value를 get, set 
* key들은 중복 불가. 한개의 key에는 하나의 value만
* key 로 사용할 수 있는 데이터형: string, symbol(ES6), object, function
  * number는 불가능

## 맵의 구체적인 개념 
* 맵은 값의 개수을 알수있는 프로퍼티가 존재하여 좀더 쉽고 명확하게 개수를 확인할수 있다.  
  
```js
let emoticon = { 
    "/와우/" : "wow.png",
    "/나우/" : "now.png",
    "/하트/" : "love.png"
}
// 객체 개수를 알아내기 
object.keys(emoticon).length;   // 3

let mapEmoticon = new Map()
    .set("/와우/", "wow.png")
    .set("/나우/", "now.png")
    .set("/하트/", "love.png")
// 객체 개수를 알아내기
mapEmoticon.size                // 3
```
* 객체는 순회하기 위해서 키를 알아낸후 순회해야하지만, 맵은 순회가능한 컬랙션이다.
* 맵에는 순회가능한 forEach 메서드가 제공되기에 간단하고 명확하게 값을 확인할 수 있다. 
  
```js
// 키-값 객체의 순환 
Object.keys(emoticon).forEach( ele => { console.log (ele)} )
Object.values(emoticon).forEach( ele => { console.log (ele)} )
// Map의 순환
mapEmoticon.forEach( (val, key) => { console.log(key, val)})
```
* 맵은 키-값의 추가와 제거에 맵은 좋은 성능을 보이는 반면, 객체는 키-값 쌍의 추가와 제거를 위한 최적화가 되어있지않아 좋은 성능을 기대하기는 어렵다. 

## Related Post
* javascript data collection - 객체 
* javascript data collection - 배열 

## References
> 자바스크립트 코딩의 기술    
> [[JS #5] ES6 Map(), Set()](https://medium.com/@hongkevin/js-5-es6-map-set-2a9ebf40f96b)
