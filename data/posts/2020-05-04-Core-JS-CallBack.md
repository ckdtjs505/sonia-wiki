---
url: https://ckdtjs505.github.io/posts/2020-05-04-Core-JS-CallBack
layout: post
title: '[Core JS] 콜백함수?'
series: 'Core JS'
date: 2020-05-04T00:00:00.000Z
author: changsun oh
tags: javascript CoreJS
comments: true
share: true
related: false
summary: 콜백 함수(Callback Function)의 개념과 제어권 위임에 대해 이해합니다.
---

## 콜백 함수

콜백함수는 다른 코드의 인자로 넘겨주는, 함수 즉 매개변수로 넘겨진 함수이다.
다른 코드의 인자로 변수가 아닌 함수가 넘어간다는 부분이 이해하기 쉽지 않다.
js는 변수에 함수를 할당할 수 있다. 쉽게 앞서 설명한 함수 함수 표현식을 떠올려보자.

> 다른 코드의 인자로 넘겨주는 함수

```javascript
let b = function () {
  console.log("b");
};
```

결국 콜백 함수는 어떠한 매개변수 값으로 함수가 전달 될때. 그 함수를 콜백 함수라 한다.

### 콜백함수의 의미

콜백함수가 왜 필요할까? 콜백함수가 가지는 의미에 대해 간단하게 알아보자.

call(부르다) + back(되돌아오다)의 함성어인 콜백함수는 문자 그대로의 의미를 가진다.
함수를 부른 곳을 다시 되돌아와서 코드를 실행하게 된다. 어떤 함수 X를 호출하면서 특정 조건일 때
Y함수(콜백함수)를 실행 하고 호출한 지점인 함수 X로 돌아가 실행한다. 즉 Y함수는 X함수에 에 `종속적`이며,
X함수는 Y함수의 `제어권`을 가지고 있다.

간단한 예시로 확인해보자

```javascript
var count1 = 0;
var timer = setInterval( () => {
  console.log(count1);
  if(++count1 > 4) clearInterval(timer);
}, 300);

실행결과
0
1
2
3

 1. 변수 count1을 선언하고 0을 할당한다.
 2. timer에는 setInterval()의 id값이 담긴다.
 3. setInterval()함수가 0.3초마다 익명함수를 실행한다.
 4. 익명함수는 count1의 값을 1씩 증가한다. setInterval()로 돌아간다.
 4. count1의 값이 4보다 커지면 clearInterval()을 호출하여 timer를 종료한다.
```

### 콜백함수의 this 바인딩

콜백 함수는 함수이다. 어떤 객체의 메서드로 호출되더라도 함수로써 호출된다.
이에따라 콜백 함수의 this는 window 객체를 바라보게 된다. 코드로 자세히 알아보자.

```javascript
var obj = {
  vals: [1, 2, 3],
  logValues: function (v, i) {
    console.log(this, v, i);
  },
};
// 메서드로써 호출 => this : obj
obj.logValues(1, 2);
// 콜백함수로써 호출 => this : window
obj.vals.forEach(obj.logValues);

실행결과
{vals: [1,2,3], logValues: func}, 1, 2
window 1
window 2

 1. obj 객체를 생성한다. 프로퍼티 vals의 값으로 배열 [1, 2, 3] 을 할당,
   프로퍼티 logValues는 this, v, i의 값을 출력하는 함수를 할당
 2. obj 프로티인 logValues 메서드를 호출, 메서드 이므로
   this는 obj를 바인딩한다.
 3. obj.vals의 값인 배열 [1, 2, 3]의 forEach 함수의 콜백으로 logValues를 실행
   콜백 함수는 this를 전역 객체에 바인딩.
```

즉 콜백 함수는 함수로 호출되기 때문에, this가 window객체를 바라본다는 문제가 있다.
이러한 문제를 해결하고자. this 바인딩을 우회 할 수 있어야한다. [this 바인딩](https://github.com/ckdtjs505/jsCoreStudy/blob/master/this.md)

### 콜백함수 this 우회

전통적인 방법으로 변수에 해당 객체 this를 할당하여, 클로져로 접근하는 방법으로 this를 우회해 보자.

```javascript
var obj = {
  name: "sonia",
  getName: function () {
    // 1. self에 this 할당
    var self = this;
    // 2. 익명 함수를 리턴
    return function () {
      console.log(self.name, this);
    };
  },
};

// 3. callback에 2항의 익명함수를 할당.
var callback = obj.getName();
// 4. 0.3이후 self.name에 접근
// 클로저로 내부 변수(self)의 값(name)을 출력
setTimeout(callback, 300);

실행결과;
sonia;
window;
```

새로운 변수 하나를 생성하고, 그 변수에 this를 할당한다. 해당 객체의 this가 할당된 변수를 사용함으로써
obj의 name의 접근할 수 있다. 해당 객체의 this를 할당한 변수에 접근하기 위해, 함수를 리턴하여 클로저로 접근하는
방법을 사용했다. 굉장히 복잡해보인다😂

속으로 이런 생각까지 든다. 그냥 this를 사용하지 않을래..
바로 해당 객체의 프로퍼티에 접근하여 값을 출력해 버리자

```javascript
var obj = {
  name: "sonia",
  getName: function () {
    // 1. 해당 객체의 프로퍼티 접근
    console.log(obj.name);
  },
};

var callback = obj.getName();
setTimeout(callback, 300);
```

이렇게 간단한 코드를 굳이 this를 써서할 필요가 있을까? 결론 부터 말하면 있다.
this를 사용하지 않고 해당 객체의 프로퍼티에 접근한 방식의 getName은 obj의 name 프로퍼티만 출력한다.
이에따라 getName 프로퍼티는 다른 객체에서 사용될 수가 없다. 즉 `재활용` 될수 없는 코드가 된다.
그래서 굳이 this를 사용하여 `재활용` 될수 있는 코드를 작성하고자 먼저 설명한 방법으로 변수에 this를 할당하여
접근하도록 한다.

> `재활용`의 여부에따라 this를 사용할지 말지 결정한다.

변수에 this를 할당하여 `재활용`되는 경우를 간단하게 코드로 알아보자.

```javascript
// 1. obj 객체 생성
var obj = {
  name: "sonia",
  getName: function () {
    // self 변수에 this를 할당하여 재활용 가능
    var self = this;
    return function () {
      console.log(self.name);
    };
  },
};

var callback = obj.getName();
setTimeout(callback, 300);

// 2. obj 객체 생성
var obj2 = {
  name: "star",
  // 1항에서 생성한 getName을 할당
  getName: obj.getName,
};

var callback2 = obj2.getName();
setTimeout(callback2, 300);

var obj3 = { name: "sujin" };

// 1항에서 생성한 getName에 this에 obj3인자로 넘김
var callback3 = obj.getName.call(obj3);
setTimeout(callback3, 300);
```

이렇게 obj.getName함수가 재활용 되는 경우를 볼 수 있었다.
이에따라 전통적인 방법의 this 우회가 많이 사용되고 있다.
하지만 단점도 있다 코드가 너무 번거롭고 불필요한 변수가 할당되고 있다는 점.
이러한 문제를 해결하고자 ES5에서 새로 만들어진 bind함수를 활용해보자.

### 2) bind 함수를 이용한 this 우회

전통적인 방법의 this 우회의 경우 어쩔수 없이 새로운 변수를 생성하고 할당해야한다는 아쉬움이 있었다.  
이러한 문제를 해결해 보고자 ES5에서 사용하는 bind 함수가 등장하게 된다.

```javascript
var obj = {
  name: "sonia",
  getName: function () {
    console.log(this.name);
  },
};
setTimeout(obj.getName.bind(obj), 300);

var obj2 = { name: "sujin" };
setTimeout(obj.getName.bind(obj2), 300);
```

이러한 방식으로 this를 바인딩할 수 있게 된다.

### 3) arrow func을 활용한 this 우회

ES6가 호환되는 환경이라면 arrow func으로도 우회할 수 있으므로 우회해보자

```javascript
var obj = {
  name: "sonia",
  getName: function () {
    // 화살표함수를 선언과 동시에 반환
    return () => console.log(this.name);
  },
};

var callback = obj.getName();
setTimeout(callback, 300);
```

arrow func은 this 바인딩 자체가 없다. 이에따라 this를 변수에 할당하거나
할 필요가 없게 된다. 왜냐 this바인딩을 하지 않으므로 상위 객체의 this를 접근하게 되기 때문이다.
this를 사용하므로 재활용 또한 가능한 코드로, 매우 탁월한 선택일 수 있다.
