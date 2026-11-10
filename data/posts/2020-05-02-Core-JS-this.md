---
url: https://ckdtjs505.github.io/posts/2020-05-02-Core-JS-this
layout: post
title: '[Core JS] this란?'
series: 'Core JS'
date: 2020-05-02T00:00:00.000Z
author: changsun oh
tags: javascript CoreJS
comments: true
share: true
related: false
summary: 자바스크립트에서 this가 실행 컨텍스트에 따라 어떻게 바인딩되는지 동작 원리를 알아봅니다.
---

## 이 글에서 다루는 것
* this의 개념을 이해한다.
* 함수내부에서 this의 동작 원리를 이해한다. 
* 메서드 내부에서 this의 동작 원리를 이해한다.
* 콜백 함수 내부에서 this의 동작 원리를 이해한다.
* 생성자 내부에서 this의 동작 원리를 이해한다. 

## 자바스크립트의 this란 무엇인가요?
* this는 어디서든 사용될 수 있다. 
* this는 **실행 컨텍스트가 생성** 될때 함께 결정된다.
> 크롬 개발자 도구(F12)에서 this를 입력해보자. 결과로 window객체가 나온다. this를 입력 할 때 전역 실행 컨텍스트가 생성되면서 전역 객체를 바라보게된다.

```
브라우저에서의 전역 객체는 `window`  
Node.js에서의 전역 객체는 `global` 
```

## 일반 함수 안에서 this는 무엇을 가리키나요?
* 함수 내부에서 this는 **전역 객체**로 결정된다. 
* **Douglas Crockford**는 이를 명백한 설계상의 오류라고 한다.  

```javascript
var outer = function () {
    var inner = function() {    
        console.log('inner' + this);
    }
    console.log('outer' + this);
    inner();
} 
outer();
```

1. 먼저 전역 컨텍스트가 생성이되고 outer()함수를 실행한다.  
2. outer() 실행 컨텍스트가 생성되면서 this는 window 를 바인딩 한다.  
  → 5 번째줄 console 실행 : outer object window
3. inner() 실행 컨텍스트가 생성되고 this는 window 를 바인딩 한다.  
  → 3 번째줄 console 실행 : inner object window

## 메서드 안에서 this는 무엇을 가리키나요?
* 메서드 내부에서 this는 **호출한 주체의 정보**로 결정된다.


```javascript
var object = {
    outer : function() {
        var inner = function(){
            console.log('inner' + this);
        }
        console.log('outer' + this);
        inner();
    }
}

object.outer();
```

1. 먼저 전역 컨텍스트가 생성이되고 object 객체를 생성한다.  
  → 12 번째줄object객체의 메서드 outer() 실행 
2. outer() 실행 컨텍스트가 생성되면서 this는 호출한 주체인 object 를 바인딩 한다.  
  → 6 번째줄 console 실행 : outer object object
3. inner() 실행 컨텍스트가 생성되고 this는 window 를 바인딩 한다.  
  → 4 번째줄 console 실행 : inner object window

> 메서드 내부에서 동작한 outer의 this는 호출한 주체인 object를 바인딩 했다.  
이에 반한 함수로서 동작한 inner의 this는 앞서 설명한 window를 바인딩 했다.  

## 콜백 함수 안에서 this는 무엇을 가리키나요?
* 콜백 함수에서의 this는 **제어권을 가지는 함수**가 결정한다.  
  * addEventListener가 제어권을 가지는 함수로써, this를 이벤트가 발상한 돔으로 결정한다. 

  ```javascript
  document.body.innerHTML = "<Button>버튼</Button>"
  document.querySelector('Button')
    .addEventListener('click', function() { console.log(this) });

  // 버튼 클릭시 - <button> 버튼 </button>
  ```
  
* **제어권을 가지는 함수**가 this를 지정하지 않는 경우 this는 **전역 객체(window)**를 바라본다.  
  * forEach가 제어권을 가지는 함수로써, this를 특별히 결정하지 않는다.    
  
  ```javascript
  let ary = [ 1, 2, 3, 4, 5];
  // forEach 콜백 함수 호출 
  ary.forEach( function(ele){
    console.log(this, ele);
  })

  /* 실행결과 
  Window 1  
  Window 2  
  Window 3    
  Window 4  
  Window 5  
  */
  ```

## 생성자 함수 안에서 this는 무엇을 가리키나요?
* 생성자 함수에서 this는 **class 객체** 즉 자기자신이 된다.  

  ```javascript 
  class dataModel {
    constructor(name){
      this.name = name;
      this.showData();
    }
    showData(){
      console.log(this);
    }
  }

  new dataModel('school');
  // 실행결과 - dataModal {name: "school"}
  ```
