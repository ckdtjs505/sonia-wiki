---
url: https://ckdtjs505.github.io/posts/2020-07-22-DevelopmentTip3
layout: post
title: '[Development Tip #3] 적절한 메서드를 발견하라'
series: 'Development Tip'
date: 2020-07-22T00:00:00.000Z
author: changsun oh
tags: Tip
comments: true
share: true
related: false
summary: hasOwnProperty로 객체 속성을 확인하는 방법과, 값의 유효성을 검사할 때 배열로 변환해 비교하는 방법을 정리합니다.
---

## hasOwnProperty

```javascript
var age = {
  one : 1,
  two : 2,
  three : 3,
  four : 4,
  five : 5
}

var human = {
  age : age.five,
  name : 'sonia'
}
```

`hasOwnProperty`는 객체에 프로퍼티를 가지고 있는지 체크한다.  
```javascript
human.hasOwnProperty('age') 은 true,  
human.hasOwnProperty('name') 은 true,  
```
=> human은 age, name을 프로퍼티로 가지고 있기 때문에 true

```javascript
human.hasOwnProperty(age.five) 은 false,  
human.hasOwnProperty('sonia') 은 false  
```
=> human은 10, sonia는 프로퍼티가 아니라 값으로 때문에 false

대부분 실무에서는 프로퍼티가 있고 없고도 중요하지만, 값을 판단하는 하는 경유가 더 많다.  
이 점을 생각해보면, 프로퍼티보다는 값을 가지고 판단하는 것이 더 중요하다.

> 사용자가 입력한 값에 대하여 올바른 값인지 판단(유효성 검사)하는 경우를 생각해보자 

```html
<form> 
  <input/>
</form>
```
```javascript
var age = {
  one : 1,
  two : 2,
  three : 3,
  four : 4,
  five : 5
}

var form = document.querySelector('form');
var input = form.querySelector('input');
var validation = (value) => Object.values(age).includes(value);

form.addEventListener('submit', () => {
  var value = parseInt(input.value);
  validation(value) ? 
    console.log(`입력한 나이는 : ${value}` ) : 
    console.log('잘못된 값을 입력했습니다')
})
```

올바른 값인지 유효성을 판단할 때는 배열로 변환하는 것이 훨씬 정확하다.
