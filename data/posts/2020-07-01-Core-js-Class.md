---
url: https://ckdtjs505.github.io/posts/2020-07-01-Core-js-Class
layout: post
title: '[Core JS] 클래스란?'
series: 'Core JS'
date: 2020-07-01T00:00:00.000Z
author: changsun oh
tags: javascript CoreJS
comments: true
share: true
related: false
summary: ES6에 도입된 클래스(Class) 문법과 기존 프로토타입 기반 상속과의 차이를 알아봅니다.
---


앞서 지금까지 프로토타입에 대해 배우면서 프로토타입을 참조함으로써 마치 상속받은 거처럼 구현되는 것처럼 보였지만,
정확히는 js에서는 상속의 개념이 없다. 이에 상속이라는 개념에 익숙하기에 많은 개발자들을 혼란스럽게 했다.
이에 따라 ES6에서는 클래스 문법이 추가가 되었다. 그러면 이제 프로토타입의 개념은 필요없나? 그건아니다.
왜냐하면 ES6미만 지원하는 브라우저에서는 프로토타입을 사용해야하기 때문에 프로토타입에 대해서도 정확하게
이해하고 넘어갈 필요가 있다.

### 클래스란

클래스란 문자그대로의 의미인 '계급','집단','집합'으로 접근하면 된다. 가령 음식을 예로 들면 고기, 생선, 과일 등등 다양한 것들이 
들어갈 수 있다. 또 과일 안에는 배, 사과, 바나나 등등이 포함된다. 여기서 음식이 제일 상위개념이고 그아래에 고기, 생선, 과일
그리고 과일 아래에 배, 사과, 바나나가 있다. 여기서 나온 모든 단어들을 클래스가 될수 있다. 

자바스크립트에서는 클래스의 개념이 존재하지 않는다. 하지만 비슷하게 동작하는 기능을 배웠는데, 눈치가 있는사람은 바로 알 수 있다. 
바로 프로토타입인데, 생성자의 프로토타입을 인스턴스가 참조받는 동작이 마치 클래스에서의 상속과 비슷하게 동작한다. 
다시정리하면 어떤 인스턴스에 프토로타입은 존재하는데 이 프로토타입은 생성자의 프로토타입을 참조한다. 프로토타입에 할당된 메서드를
우리는 프로토타입 메서드라고 부르며. 인스턴스에 바로 할당된 메서드를 인스턴스 메서드라고 한다. ㅎㅎ 
물론 둘다 메서드이지만 어디에 할당되었는지에 따라 부르는 명칭이 다르다. 

정리하면 자바스크립트에서의 클래스의 개념이 존재하지는 않지만, 비슷하게 해석할 수 있었다. 

```js
// 생성자
let Person = function (name, age) {
  this.name = name;
  this.age = age;
}

// 프로토타입 메서드
Person.prototype.getName = function(){
  return this.name;
}

// 스태틱 메서드
Person.isPerson = function(instance) {
  if(typeof instance.name !== "string" || typeof instance.age !== "number" )
    return false;   
  return true;
}

let changsun = new Person ("changsun", 27);
console.log(changsun.getName());            // changsun
console.log(Person.isPerson(changsun));     // true

```
Person이라는 생성자를 만들어 매개변수로 name과 age를 넘긴다. 
이름을 가져오는 프로토타입 메서드 getName과 Person인지 확인하는 스태틱 메서드 isPerson을 구현했다.
사용하면서 알수 있었겠지만, 프로토타입 메서드는 인스턴스에서 바로 사용이 가능한 반면 스태틱 메서드의 경우
생성자 함수를 호출해서 사용할 수 있었다. 

### 클래스 상속
자바스크립트의 클래스의 개념에 대해 알아보았다. 이번에는 자바스크립트 클래스의 상속에 대해 알아보자.
클래스 상속은 객체지향에서 가장 중요한 개념중 하나이다. 이에 따라 자바스크립트 또한 개발자들에게 친숙한 형태로 
상속을 구현에 내는 것이 주요한 관심사였다. 현재 ES6에서는 class 문법을 지원함으로써 이러한 문제가 해결이 되었지만,
ES5이전에는 그렇지 못했다. ES5에서 부터 클래스의 상속이 어떻게 만들어져 갔는지, 그리고 최근 자바스크립트에서는 
어떻게 구현하여 사용되고 있는지 알아보자. 

먼저 ES5에서의 클래스 상속에 대해 간단하게 구현해보자. 전에 프토토타입 체인에 대해 살폈었다. 
핵심은 프로토타입 체인에 있으므로, 혹시 생각이 안나는 분들은 간단하게 훓고 오는것도 좋은 방법이라 생각한다.

```js
// 생성자
let Person = function (name, age) {
  this.name = name;
  this.age = age;
}

// 프로토타입 메서드
Person.prototype.getName = function(){
  return this.name;
}

// 스태틱 메서드
Person.isPerson = function(instance) {
  if(typeof instance.name !== "string" || typeof instance.age !== "number" )
    return false;   
  return true;
}

let Korean = function (name, age){
  Person.call(this,name,age);
  this.locale = "ko";
}

Korean.prototype = new Person();

let changsun = new Korean("changsun", 27);
console.log(changsun.getName());            // changsun
console.log(changsun.locale);               // ko
console.log(changsun.age);                  // 27
```

앞서 만든 Person 객체를 사용하여 구현해 보았다. 핵심은 프로토 타입에 생성자를 넣는 방식인데. 
프토토 타입의 값을 `__proto__`가 참조하기에 마치 상속하는 것처럼 동작한다.
그러나 위 코드만으로 완벽한 클래스가 생성되었다고 말하기는 어렵다. 

configurable의 값이 false인 경우 프로터티가 삭제되지 않지만, 상속을 이용해여 구현한 모든 프로퍼티는 
configurable 값에 상관없이 다 삭제 가능해서 문제가 된다. 즉 클래스의 값이 인스턴스에 영향을 줄 수 있는 가능성이 생긴다.

뿐 아니라 먼가 이상함을 느낄수 있는데 devTool을 열고 
```js
console.dir(changsun);
```
을 입력해보자 그러면 결과 값으로 
```html
Korean 
  - age : 27
  - 
  - name : "changsun"
  - __proto__ : Person 
      - age : undefined
      - name : undefined
``` 

Person의 age와 name의 값이 undefined가 되어서 출력된다 왜그럴까? 
그것보다 우선적으로 우리가 알고있는 클래스의 상속이 일어나면 위와같은 모습이 아니다.
```html
Korean 
  - locale : "ko"
  - name : "changsun"
  - __proto__ : Person 
      - age : 27
      - name : "changsun"
```
이렇게 되어야 중복도 없고 진정한 클래스의 상속이라 할 수 있다. 

먼저 왜 Person의 age와 name의 값이 undefined가 되는지 알아보자 

위와 같이 진정한 클래스의 상속이 일어나도록 구현해보자. 

```js
let Bridge = function () {} ;
Bridge.prototype = Person.prototype;
Korean.prototype = new Bridge;
Object.freeze(Korean.prototype);

let changsun = new Korean("changsun", 27);
console.dir(changsun);
```

너무 어렵다ㅠ 클래스를 실무에서 구현해서 사용하는 일은 많이 없다고 판단되어
여기에서 정리를 마무리 하겠다. 
