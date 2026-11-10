---
url: https://ckdtjs505.github.io/posts/2020-06-21-Core-JS-Prototpye
layout: post
title: '[Core JS] 프로토타입이란?'
series: 'Core JS'
date: 2020-06-21T00:00:00.000Z
author: changsun oh
tags: javascript CoreJS
comments: true
share: true
related: false
summary: 자바스크립트 프로토타입(Prototype) 체인과 객체 지향 상속 모델의 핵심을 이해합니다.
---

프로토타입!? 많이 생소한 단어다. 자바스크립트는 프로토타입 기반 언어라고들 하지만, 프로토 타입이 도대체 먼지 감을 잡기가 쉽지가 않다.
대부분의 언어는 클래스 기반의 언어로 배웠고, '상속'이라는 개념이 있어 비슷한 클래스를 쉽게 만들 수 있었다. 
그래서 많이들 자바스크립트가 어렵다고 느끼는 이유 중 하나가 생소한 개념인 프로토타입 기반의 언어라 그렇다. 

솔직하게 자바스크립트에서 프로토타입의 개념의 필요성을 느끼지 못하고 있다.
개념적으로는 중요하지만, 실무에서 프로토타입을 과연 몇번이나 쓰게 될까? 
최근 자바스크립트에서는 클래스 기능을 지원하고 있어, 프로토타입의 개념을 모른다고 큰 문제가 되거나 할 일이 없다.

비록 프로토타입이라는 개념이 어렵고 크게 필요성을 느끼고 있지는 못하지만, 
어떤 역할을 맞고 있고, 어떠한 특성이 있는지 정도는 알고 넘어가자 ㅎㅎ 

### 프로토타입 개념

```js
let Person = function (name, age){
    this.locale = "ko";
    this.name = name;
    this.age = age;
}

Person.prototype.getLocale = function(){
    return this.locale;
}

let man = new Person("changSun", 27);
console.log(man.getLocale, man.__proto__.getLocale, Person.prototype.getLocale);
console.log(man.getLocale(), man.__proto__.getLocale(), Person.prototype.getLocale());
```

결과값을 살펴보자.
첫번째 콘솔의 결과값은 
```js
ƒ (){
    return this.locale;
} ƒ (){
    return this.locale;
} ƒ (){
    return this.locale;
}
```
`man.getLocale`, `man.__proto__.getLocale`, `Person.prototype.getLocale` 모두 같은 메서드가 할당되었다.
어떠한 과정으로 메서드가 할당 되었는지 간단하게 순서로 알아보자.  

1. `Person 생성자` 함수를 호출 
2. `Person 생성자` 함수에 정의된 내용으로 새로운 `man 인스턴스` 을 생성
3. `man 인스턴스` 에 `__proto__ 프로퍼티` 자동 부여.
4.  `__proto__ 프로퍼티`는 `Person 생성자`의 `prototype 프로퍼티`를 참조한다.

이렇게 인스턴스에는 `__proto__`, 생성자에 `prototype`는 서로 같은 함수(메서드)를 공유하게 된다. 
`prototype`은 객체 내부에서 인스턴스가 사용할 메서드를 저장한다. 

두번째 콘솔의 결과값은 
```js
ko undefined undefined
```
`man` , `man.__proto__`, `prototype` 은 모드 같은 함수를 할당하고 있는 것을 첫번째 콘솔에서 알아보았다.
그러나 놀랍게도 `man`객체만 정확한 결과값을 출력했다. 왜그럴까? 바로 this의 동작 원리 때문인데.
`man.__proto__`에서의 this는 다른 값을 바라보고 있기 때문이다. 여기서 헷갈리는 부분은 
`man` 에는 함수가 선언되어 있지 않음에도 오히려 올바른 값을 반환하고 있기 때문이다.
가능하게 된 이유는 별겨아닌 `__proto__` 프로퍼티가 생략 가능하도록 정의 되어 있기 때문이다. 
물론 생략 가능한 프로퍼티에 대해 거부감을 느낄 수 있겠지만, 만든분이 그렇게 만들었다

결론적으로 new 연산자로 생성된 인스턴스는 `__proto__`라는 생략가능한 프로퍼티를 생성자의 `prototype`을 참조한다.

### constructor 프로퍼티

생성자 함수의 `prototype` 객체 내부에는 `constructor` 프로퍼티가 있다.
`prototype`을 참조하게 되는 `__proto__`또한 `constructor` 프로퍼티를 가진다.
`constructor`에는 어떤 정보가 들어갈까? 문자 그대로의 의미인 생성자 함수를 참조한다. 
왜냐하면 주어진 인스턴스의 원형을 파악하는데 필요하기 때문이다. 

```js
let arr = [1,2];
console.log(arr.__proto__.constructor);     // f Array()
console.log(arr.constructor);               // f Array()
console.log(Array.prototype.constructor);   // f Array()
```
예시처럼 `__proto__`를 생략하지 않고 사용할수 있지만, 생략하는게 훨씬 직관적이다.

```js
let arr = [1,2];
console.log(arr.constructor);               // f Array()

let arr2 = arr.constructor(3,4);
console.log(arr2);                          // [3,4]
```
arr를 만든 원형인 Array함수(생성자)에 접근하여 새로운 Array를 만들었다.  
신기하고 재미있는 개념이라 생각된다. 

그러나 constructor가 인스턴스의 원형을 보장하지는 않는다. 
어떠한 경우인지 한번 알아보자 

```js
let arr = [1,2];

let newConst = () => { console.log("새로운 생성자") }
arr.constructor = newConst
console.log(arr.constructor);               // () => { console.log("새로운 생성자") }

let arr2 = arr.constructor(3,4);
console.dir(arr2);                          // undefined
console.dir(arr);                           // Array(2)
```

4번째 줄에서 새로운 생성자 함수가 할당 되었다. 이에따라 8번째줄 console은 undefined를 출력한다. 
참조하는 함수의 원형이 바귄 arr의 속성이나 타입이 바뀌었을까? 9번째줄 console을 확인해 보면 
그렇지 않다는 것을 알 수있다. 항상 constructor가 생성자정보를 가지고 있다고 의존하는 건 안전하지 않다. 

## 프로토 타입 체인

프로토 타입 체인은 문자 그대로 프로토타입이 체인처럼 연결되어 있는것을 말한다. 
`__proto__`가 생략이 가능하기 때문에 약간의 혼동이 있을 수 있지만, 차근차근 알아보자


### 메서드 오버라이드 

```js
let Person = function (name){
    this.name = name;
}

Person.prototype.getName = function () {
    return this.name;
}

let sujin = new Person('수진');
sujin.getName = function(){
    return '박'+ this.name;
}

console.log(sujin.getName());
```
당연히 getName은 새롭게 덮혀졌으므로 실행결과는 `박수진`이 나오는 것이 정상이다.
즉 가장 가깝게 선언된 프로토타입에 접근하여 실행한다. 

## 프로토 타입 체인

`__proto__` 프로퍼티가 연쇄적으로 이어져 있는 것을 `프로토타입 체인`이라고 한다.  
앞서 `프로토타입`에서 생성된 함수를 `__proto__`가 참조한다고 배웠다. 
그렇다면 `프로토타입 체인`은 느낌상 `프로토타입`이 여러가지로 맞물려 있을꺼라고 짐작이된다.
`인스턴스`기준에서 생각해보면 `__proto__ 체인`인 것이며, `__proto__`에 단계별로 접근하면서 어떤 체인이 있는지 확인해 보자.  

먼저 배열을 알아보자.

```js
console.dir([1,2].__proto__);                       // Array(0)
console.dir([1,2].__proto__.__proto__);             // Object
console.dir([1,2].__proto__.__proto__.__proto__);   // null
```

첫번 째 콘솔은 Array를 반환한다. 결과값을 통해 [1,2]은 배열 프로토타입 상속 받는 걸 알 수 있다.
두번 째 콘솔은 Object를 반환한다. 결과값을 통해 Array는 Object 프로토타입 상속 받는 걸 알 수 있다. 
마지막 콘솔은 null을 반환하는데. Object는 상속받는 프로토타입이 없다. 

즉 다시 말해 [1,2]에는 Object 중에서 Array라는 의미로 생각해도 된다. 
이렇게도 생각할수 있는데 [1,2]에서 Ojbect 프로토타입을 사용할 수 있다.

```js
console.log([1,2].hasOwnProperty(1));               // true
console.log([1,2].push(3));                         // [1,2,3]
```

첫번째 콘솔에서 hasOwnProperty 함수는 object 프로토타입 함수이지만 사용 할 수 있다는 것을 알 수 있다.
이렇게 프로토타입 체이닝을 통해 상속받은 최상단의 프로퍼티를 사용할 수 있다. ㅎㅎ

어떤 생상자 함수든 object를 상속받아 생성된다. 어찌보면 당연한건데 모든 생성된 인스턴스는 객체이기 때문이다.
이런 생각을 할수도 있는데. object.prototype을 추가로 생성하면, 모든 생성자에 추가가 된다.

```js
Object.prototype.console = function() {
    console.log("값은 : " +this);
}  
[1,2].console();            // 값은 : 1, 2
"12".console();             // 값은 : 12
```

이와는 반대로 객체에서만 사용하고자 할때가 있다. 이와 같은 경우로는 Object의 스태틱 메서드로 부여해야한다.

```js
Object.console = function(input) {
    console.log("값은 : " + input);
}  
Object.console([1,2]);            // 값은 : 1, 2
Object.console("12");             // 값은 : 12
[1,2].console();                  // undefined
```
스태틱 멕서드로 부여하기에 아쉬운 부분 몇몇 가지가 보인다. 생성자 함수와 인스턴스는 `this`를 공유할수 없기에 인스턴스 인자로
넘겨주는 모습을 확인 할 수 있다. 부득이게 객체만을 대상으로 동작하는 경우를 접할 경우가 없기에 이렇게만 알고 넘어가자 

### 다중 프로토 타입 체인

먼저 문자 의미 그대로 여러개의 프로토 타입이 묶여 있는 경우를 말한다. 
간단하게 코드를 통해 알아보자. 

```js
let sameAry = function() {
    let args = Array.prototype.slice.call(arguments);
    for( let i = 0 ; i < args.length ; i++ ) {
        this[i] = args[i];
    }
    this.length = args.length;
}

let ary = new sameAry();
ary.push(1)             // undefined

sameAry.prototype = [];
let ary2 = new sameAry(); 
ary2.push(1);           // sameAry[1]
```

sameAry는 유사배열 객체를 생성하는 생성자이다. sameAry 생성자에는 따로 프로토 타입을 추가하지 않고 
배열을 프로토 타입에 넣었다. 이에따라 배열 프로토타입을 사용할 수 있게 되었다. 
