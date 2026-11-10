---
url: https://ckdtjs505.github.io/posts/2020-05-05-Core-JS-CallBackHall
layout: post
title: '[Core JS] 콜백지옥?'
series: 'Core JS'
date: 2020-05-05T00:00:00.000Z
author: changsun oh
tags: javascript CoreJS
comments: true
share: true
related: false
summary: '콜백 지옥(Callback Hell)의 문제점과 이를 해결하기 위한 Promise, async/await 패턴을 알아봅니다.'
---

앞서 콜백함수에 대해 알아보았다. 콜백함수를 간단하게 인자로 넘겨지는 함수로 배웠다.
함수이기에 this는 window 객체를 바라보게 되었고, 이러한 문제를 해결하고자
변수를 활용, bind, 화살표함수를 이용해 바인딩문제를 해결하였다.

함수가 인자로 넘겨짐으로써 생기는 보이는 하나의 문제가 있다.
콜백함수가 인자로 넘겨짐으로써 코드의 들여쓰기 수준이 감당할수 없을 정도로 깊어지는 현상이 생긴다.
이러한 현상을 콜백 지옥이라고 부른다. 주로 `이벤트처리`, `서버 통신`에서 이런 형태가 많이 등장한다.

간단한 배경을 살펴보자면 js는 비동기적인 코드로 현재 실행중인 코드 완료 여부는 상관없이 다음 코드를 실행한다.
그에 반해 동기적인 코드는 실행중인 코드를 완료한 이후에 실행하는 코드를 의미한다. 나날이 웹의 복잡도가
높아지면서 비동기적인 코드의 비중이 예전보타 훨씬 높아지게 되면서 콜백 지옥에 훨씬 빠지기 쉬워졌다.

간단한 콜백지옥의 예시를 보자

```javascript
const body = document.body;
document.body.innerText = '로딩중입니다';
let text = [];
setTimeout(
  (val) => {
    text.push(`${val} 완료`);
    body.innerHTML = text;

    setTimeout(
      (val) => {
        text.push(`${val} 완료`);
        body.innerHTML = text;

        setTimeout(
          (val) => {
            text.push(`${val} 완료`);
            body.innerHTML = text;

            setTimeout(
              (val) => {
                text.push(`${val} 완료`);
                body.innerHTML = text;
              },
              1000, "게임시작"
            );
          },
          1000, "유저 선택"
        );
      },
      1000, "서버설정"
    );
  },
  1000, "환경설정"
);
```

1초마다 게임정보를 수집하고 출력한다. 완벽하게 동작한다.
하지만 값이 전달되는 순서가 아래서 위로 향하고 있어서 보기에 많이 불편하다.

이러한 가독성을 해결하기 위한 가장 간단한 방법으로 `익명함수`를 `기명함수`로 변환하여
실행하는 방법이 있다. 간단하게 구현해보자 

```javascript
const body = document.body;
document.body.innerText = '로딩중입니다';
let text = [];

let setConf = (val) => {
  text.push(`${val} 완료`);
  body.innerHTML = text;
  setTimeout(setServer, 1000, "서버설정");
}

let setServer = (val) => {
  text.push(`${val} 완료`);
  body.innerHTML = text;
  setTimeout(setUser, 1000, "유저설정");
}

let setUser = (val) => {
  text.push(`${val} 완료`);
  body.innerHTML = text;
  setTimeout(setGame, 1000, "게임설정");
}

let setGame = (val) => {
  text.push(`${val} 완료`);
  body.innerHTML = text;
}

setTimeout(setConf, 1000, "환경설정");
```

첫번째로 작성한 콜백함수보다는 훨씬 가독성있어졌지만, 여전히 아쉬운 부분이 존재한다. 
먼저는 일회성 함수를 전부 변수에 할당하는것이 아쉽다. 이러한 아쉬운 부분을 해결하고자 
자바스크립트는 끊임없이 노력해왔다. ES6에서는 Promise, Generator가 ES2017에서는 async/await가
도입되었다. 

첫번째로 ES6에서 추가된 Promise를 활용하여 위의 예제를 변경해보자. 

```javascript
const body = document.body;
document.body.innerText = '로딩중입니다';
let text = [];
new Promise(function(resolve){
  setTimeout( (val) => {
    text.push(`${val} 완료`);
    body.innerHTML = text;
    resolve();
  }, 1000, "환경설정");
}).then(function(){
  return new Promise(function(resolve){
    setTimeout( (val) => {
     text.push(`${val} 완료`);
     body.innerHTML = text;
     resolve();
    }, 1000, "서버설정");
  })
}).then(function(){
  return new Promise(function(resolve){
    setTimeout( (val) => {
     text.push(`${val} 완료`);
     body.innerHTML = text;
     resolve();
    }, 1000, "유저설정");
  })
}).then(function(){
 return new Promise(function(resolve){
    setTimeout( (val) => {
     text.push(`${val} 완료`);
     body.innerHTML = text;
     resolve();
    }, 1000, "게임설정");
  })
})
```
먼가 더 복잡해 보이는거 같다. 왜 복잡하게 Promise객체를 생성해서 진행하는가?에 대한
의문점또한 들 수 있다. Promise 객체를 이용하여 비동기를 처리하게 되면, ~~예외처리에도 대응할 수 있는 코드가된다. 그만큼 안전한 코드가 된다는 의미를 가진다~~. Promise 객체를 사용하면 resolve()가 있어 콜백 함수가 종료 후에 비동기적으로 실행할수 있다.

```js
const body = document.body;
document.body.innerText = '로딩중입니다';
let text = [];

new Promise(function(resolve){
  setTimeout( (val) => {
    text.push(`${val} 완료`);
    body.innerHTML = text;
    resolve("test");
  }, 2000, "환경설정");
}).then( (data) => {
 alert(data); //      test
 return data;   
}).then( (val) => {
  body.innerHTML = `${val}`;    // test
})
```

then으로 넘어갈수 있는 경우는 resolve를 통해 결과값을 전달하여 넘어갈수도 있지만, 
콜백함수가 아닌 경우에는 굳이 resolve를 사용하지 않고 return 값으로 전달할 수 있다. 
