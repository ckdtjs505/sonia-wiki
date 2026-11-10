---
url: https://ckdtjs505.github.io/posts/2020-05-06-Core-JS-Closure
layout: post
title: '[Core JS] 클로저란?'
series: 'Core JS'
date: 2020-05-06T00:00:00.000Z
author: changsun oh
tags: javascript CoreJS
comments: true
share: true
related: false
summary: 자바스크립트의 핵심 개념인 클로저(Closure)의 원리와 실용적인 활용 방법을 다룹니다.
---

## 이 글에서 다루는 것

- 클로저의 의미 및 원리를 이해한다.
- 클로저의 문제점과 해결방법을 이해한다.
- 클로저의 다양한 사용방법을 이해한다.

## 자바스크립트 클로저란 무엇인가요?

- 클로저는 함수와 함수가 선언된 **어휘적 환경**의 조합이다. [출처 : MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Closures)

  > **어휘적 환경(LexicalEnvironment)**은 실행 컨텍스트에서 유효범위인 스코프가 결정되며, 스코프 체인이 가능하게 하는 역할을 한다.

- 어떤 함수 A에서 선언한 변수 a를 참조하는 내부함수 B를 외부로 전달하는 경우 A의 실행 컨텍스트가 종료된 이후에도 변수 a가 사라지지 않는 현상
- 이미 생명 주기가 끝난 외부 함수의 변수를 참조하는 함수
- GC(가비지 컬렉터)는 참조하는 값이 하나라도 있다면 그 값을 수집 대상에 포함시키지 않기 때문.

## 클로저는 어떤 코드에서 만들어지나요?

### 1. return을 이용한 클로저

```javascript
function outer() {
  let a = 0;
  function inner() {
    console.log(++a);
  }
  return inner;
}
let smallInner = outer();
smallInner();
smallInner();

/*
    실행결과
    1
    2
  */
```

1.  8번째 줄 outer 함수를 실행하면서 변수 a에 0을 할당하고 inner 함수를 smallInner에 반환.
2.  9번째 줄 smallInner가 변수 a에 접근 후 1을 증가하여 1을 출력.
3.  10번째 줄 smallInner가 변수 a에 접근 후 1을 증가하여 2을 출력.

> outer에서 선언된 변수 a가 사라졌음에도 inner 함수에서 접근하여 값이 증가 되는것을 확인할 수 있다.

### 2. setInterval의 콜백 함수 이용한 클로저

```javascript
function outer() {
  let a = 0;
  let intarvalId = null;
  let inner = function () {
    if (a < 5) console.log(++a);
    else clearInterval(intarvalId);
  };
  intarvalId = setInterval(inner, 1000);
}
outer();
/*
  실행결과 
  1  2  3  4  5
*/
```

> setInterval 함수의 첫번째 인자로 콜백함수인 inner 함수를 매개변수로 전달한다. 클로저가 발생하여 외부함수에 a 변수를 찾고, 외부함수 outer에 a가 할당 되어 있으므로, a를 참조하여 실행한다.

### 3. addEventListener의 콜백 함수 이용한 클로저

```javascript
function outer() {
  let count = 0;
  const button = document.createElement("button");
  button.innerHTML = "CLICK";
  button.addEventListener("click", function inner() {
    console.log(++count);
  });

  document.body.appendChild(button);
}

outer();
// CLICK 버튼 클릭시 count 값 증가출력
```

> button dom을 생성하여 inner함수로 이벤트를 등록한다. inner함수는 count값을 증가후 console에 출력하는데, 이때 클로저가 발생하여 outer count에 접근하여 count값을 증가하여 출력할 수 있게 된다.

## 클로저는 메모리 누수를 일으키나요?

- 클로저 사용시 특정 변수를 참조하여 **GC(가비지 컬렉터)**의 수거 대상이 되지 않아 메모리의 누수 발생
- GC의 수거 대상이 되도록 참조 카운트를 0 (NULL, undefined)으로 할당

```javascript
function outer() {
  let a = 0;
  function inner() {
    console.log(++a);
  }
  return inner;
}
let smallInner = outer();
smallInner();
smallInner();
smallInner = null;

/*
  실행결과
  1
  2
*/
```

> smallInner를 null로 참조 하여 GC의 수거 대상이 되도록 한다.

### 클로저와 메모리 관리

지금까지 클로저에 대해 간단하게 알아보았다. 클로저로 실행이 끝난 외부 함수의 변수에 접근 할 수 있수 있다 배웠다.좀더 정확하게는 **가비지 컬렉터**가 어떤 값을 하나라도 참조하는 값이 있다면, 그 값은 수집 대상에 포함시키지 않게 된다. 이에따라 클로저를 사용하게 될수록 메모리 누수가 발생하게 된다. 이런 이유로 클로저 사용을 조심해야한다는 사람들도 있다.

이러한 메모리 누수를 해결하기 위한 간단한 관리방법을 알아보자.
관리방법이라고 하니 엄청나 보이지만, 아주 간단하다. 클로저를 통해 접근한 지역변수를 다 사용했다면 메모리를 소모하지 않도록 참조 카운트를 0으로 만들면 된다. 그러면 언젠가 **가비지 컬렉터**가 수거해 갈 것이고, 소모되었던 메모리는 회수되게 된다. 참조 카운트를 0으로 만드는 방법으로 **참조형**이 아닌 **기본형**데이터(null, undefined)를 할당하게된다. 참조 카운트에 **기본형**데이터를 넣는다는것은 이전에 참조하고 있던 함수를 끊는다는 것과 동일한 의미를 가진다.

앞에서 배웠던 예시들에 메모리 해제 코드를 추가해보자.

```javascript
function outer() {
  var a = 0;
  function inner() {
    console.log(++a);
  }
  return inner;
}
var smallInner = outer();
smallInner();
smallInner();
// smallInner에 outer함수의 inner참조를 끊는다.
smallInner = null;

function outer() {
  var a = 0;
  var intarvalId = null;
  var inner = function () {
    if (a < 5) {
      console.log(++a);
    } else {
      clearInterval(intarvalId);
      // inner 변수의 익명함수 참조를 끊는다.
      inner = null;
    }
  };
  intarvalId = setInterval(inner, 1000);
}
outer();

function outer() {
  var count = 0;
  const button = document.createElement("button");
  button.innerHTML = "CLICK";
  button.addEventListener("click", function inner() {
    console.log(++count);
  });
  // 카운트의 제한이 없으므로 식별자의 참조를 끊을 수 없다.
  document.body.appendChild(button);
}
```

## 클로저는 실무에서 어디에 쓰나요?

### 첫째. 콜백 함수 내부에서 외부 데이터를 사용할때

```javascript
let items = ["faith", "love", "hope"];
let $ul = document.createElement("ul");

items.forEach(function (item) {
  let $li = document.createElement("li");
  $li.innerHTML = item;

  $li.addEventListener("click", function () {
    alert("click" + item);
  });

  $ul.appendChild($li);
});

document.body.appendChild($ul);
```

1. 4번째줄 익명의 콜백함수는 items의 개수만큼 반복 후 종료한다.
2. 8번째줄 익명의 콜백함수는 item라는 외부변수를 사용하고 있으므로 클로저가 있다.
3. 4번째 줄의 콜백함수의 실행컨텍스트가 끝났음에도 외부 변수인 item 에 접근할수 있게된다.

더나아가 8번째 줄 함수가 콜백 함수로만 쓰이는 것이 아니라, 다양하게 쓰이게 된다면 외부로 분리해야 하는 경우가 생긴다.

```javascript
let items = ["faith", "love", "hope"];
let $ul = document.createElement("ul");

let alertItem = function (item) {
  alert("click" + item);
};

items.forEach(function (item) {
  let $li = document.createElement("li");
  $li.innerHTML = item;
  $li.addEventListener("click", alertItem);
  $ul.appendChild($li);
});

document.body.appendChild($ul);
/* 
  실행결과
  click[object MouseEvent]
*/
```

> 의도하지 않았던 [object MouseEvent]라는 값이 나왔다. 그 이유는 왜냐하면 콜백함수의 첫번째 인자는 addEventListener가 주입하기 때문이다. 이러한 문제를 해결하기 위해서, 함수를 반환하고 인자의 값을 바꿀수 있도록 도와주는 bind 메서드를 활용하여 간단하게 수정할 수 있다.

```javascript
let items = ["faith", "love", "hope"];
let $ul = document.createElement("ul");

let alertItem = function (item) {
  alert("click" + item);
  console.log(this); // null 출력
};

items.forEach(function (item) {
  let $li = document.createElement("li");
  $li.innerHTML = item;
  $li.addEventListener("click", alertItem.bind(null, item));
  $ul.appendChild($li);
});

document.body.appendChild($ul);
/* 
  실행결과 
  faith 클릭시 - clickfaith 
  love 클릭시 - lovefaith 
  hope 클릭시 - hopefaith 
*/
```

> bind를 이용하여 다른 객체를 주입하는 문제를 해결했지만, 하지만 this의 값이 바뀐다는 아쉬운 부분도 존재한다. this값이 바뀌면 안된다면, 고차함수를 활용하여 해결할 수 있다.

```javascript
let items = ["faith", "love", "hope"];
let $ul = document.createElement("ul");

let alertItem = function (item) {
  return function () {
    alert("click" + item);
    console.log(this); // 선택된 dom 출력
  };
};

items.forEach(function (item) {
  let $li = document.createElement("li");
  $li.innerHTML = item;
  $li.addEventListener("click", alertItem(item));
  $ul.appendChild($li);
});

document.body.appendChild($ul);

/* 
  실행결과 
  faith 클릭시 - clickfaith 
  love 클릭시 - lovefaith 
  hope 클릭시 - hopefaith 
*/
```

> alertItem은 함수를 리턴한다. 리턴된 함수는 alert을 띄어주게된다. 이때 item 값은 외부변수의 값을 참조하여 만들어지므로 클로저가 존재한다. 이렇게 콜백 함수 내부에서, 외부 데이터를 사용하는 방법에 대해 알아보았다.

### 둘째. 접근 권한 제어

- js의 **접근 권한**에는 **public**,**private**,**protected**로 구성되어있다.
  - **public**은 내부 외부에서 모두 접근이 가능
  - **private**는 내부에서만 접근이 가능, 외부에서는 노출되지도 않아 접근하지 못함
- return한 변수들은 **public**데이터가 되고, return 되지 않은 변수들은 **private**데이터가 된다.
  - return한 변수들은 공개 변수이며, 그렇지 않음 변수들은 비공개 변수가 된다.
- 클로저는 return 으로 외부 함수의 변수 접근할 수 있기 때문
- 클로저는 외부 스코프에서 특정 함수 내부의 특정 변수에 대한 접근 권한을 부여할 수 있다

```javascript
function outer() {
  let a = 0;
  let inner = function () {
    let b = 0;
    console.log(++a, b);
  };
  return inner;
}
var outer2 = outer();
outer2();
```

> outer함수는 외부로 부터 철저히 격리된 공간이다. outer함수를 실행할수는 있지만, outer함수 내부의 변수에는 접근할수 없다. 만약 outer함수의 내부의 변수를 변경하고 싶으면 outer함수가 return한 정보로만 접근 및 변경 할 수 있게 된다.

inner함수는 내부 외부에서 모두 접근이 가능하고, outer함수의 a는 내부에서만 접근이 가능하므로 **public**데이터는 **inner()** 함수이며, **private**데이터는 **a** 임을 알수있다.

### 셋째. 부분 적용 함수

- 부분 적용 함수는 문자 그대로 부분만 적용하여 기억하는 함수이다.
- 다시말해 10개의 인자를 받는 함수가 있는데, 미리 5개의 인자만 받아 기억했다가 나중에 5개의 인자를 받으면 실행 결과를 얻을수 있게 되는 함수이다.
- this 우회할때 배웠던 bind 메서드의 실행결과 경우에 따라 부분 적용 함수가 된다.

```js
let add = function () {
  let result = 0;
  for (let i = 0; i < arguments.length; i++) {
    result += arguments[i];
  }
  console.log(this); // window
  return result;
};

let addPartial = add.bind(null, 1, 2, 3, 4, 5); // bind 함수로 저장
console.log(addPartial(6, 7, 8, 9, 10));
/*
 실행 결과 
  window
  55
*/
```

> 물론 위와 같은 방법으로 부분적용함수를 구현할 수 있으나, 실무에서 this의 값이 변경되는건 리스크다 크다. 따라서 클로저를 활용하여 this의 값이 변경되지 않도록 구현해보자.

```js
let partial = function () {
  // 인자값 저장
  let originalPartialArgs = arguments;
  // 첫번째 인자는 함수
  let func = originalPartialArgs[0];
  // 인자값 체크
  if (typeof func !== "function") {
    throw new Error("첫번째 인자가 함수가 아닙니다");
  }

  return function () {
    // 부분 함수의 인자 값
    let partialArgs = [...originalPartialArgs].slice(1);
    // 새로운 인자 값
    let restArgs = [...arguments];
    // 전달할 인자들을 모아 전달
    return func.apply(this, partialArgs.concat(restArgs));
  };
};

let add = function () {
  let value = 0;
  for (let i = 0; i < arguments.length; i++) {
    value += arguments[i];
  }
  return value;
};

let addPartial = partial(add, 1, 2, 3);
console.log(addPartial(4, 5));
```

1. **partial** 함수는 첫번째 인자가 함수인지 아닌지 판별 한후 함수를 반환단다.
2. 반환된 함수는 **addPartial**에 할당된다.
3. **addPartial**에 인자로 4,5를 전달한다.
   - originalPartialArgs(원본 인자값)에 클로저가 발생
   - **partial**가 수명이 끝났음에도 클로저로 **originalPartialArgs를** 사용한 값을 할당
   - 이전 인자와 새로받은 인자를 합친 배열은 실행

### 넷째. Debounce

- 디바운스는 동일한 이벤트가 여러번 발생한 경우 전부처리하지 않고 마지막에 발생한 이벤트에 대해 한번만 처리.
- 프론트엔트 최적화에 큰 도움을 주는 기능.
- 실전에서 정말 많이 사용

```js
let debounce = function (event, func, wait) {
  let timeoutId = null;
  console.log(event, func, wait);
  return function (event) {
    console.log(event, "event 발생");
    clearTimeout(timeoutId);
    timeoutId = setTimeout(func.bind(this, event), wait);
  };
};

var resizeHandler = function (e) {
  console.log("wheel event 처리");
};

window.addEventListener("resize", debounce("resize", resizeHandler, 500));
```

1. resize 이벤트에 콜백 함수로 debounce를 할당
2. 이벤트 발생시 debounce 함수를 콜백으로 실행
3. 실행한 익명함수에 EVENT 객체를 주입 timeoutId에 할당된 timeOut 제거
   - **timeoutId**에 클로저 발생
   - debounce 함수가 실행이 끝났음에도 **timeoutId**에 접근
4. wait 한 시간만큼 지연 후 func 함수 실행

### 다섯째. 커링 함수

- 여러 개의 인자를 받는 함수를 하나의 인자만 받는 함수로 나눠서 순차적으로 실행하게 하는 함수
- 원하는 시점까지 지연시켰다가 실행하는 것이 요긴한 상황이라면 쓰기에 적합
  - 실제적으로 개발단계에서 많이 사용해보지는 않았다. 굳이 여러개의 인자를 받는 함수를 하나의 인자만 받는 함수로 나눠서 순차적으로 실행할 필요가 있을까?
- 그러한 경우가 얼마나 있을까? 그러한 경우로 Flux 아키텍처 구현체 중 Redux의 미들웨어에서 사용된다고 한다.
  - 아키텍처 공부할 때 유용하게 사용될수 있을꺼 같으니까 일단 개념적으로만이라도 알아두자

```js
const discounter = discount => price => price * (1 - discount);

const tenPercentOff = discounter(100);
tenPercentOff(100); // 90
```

첫번째 매개변수 discount값을 저장하여 사용할 수 있다.

> 참조 : 코어 자바스크립트
