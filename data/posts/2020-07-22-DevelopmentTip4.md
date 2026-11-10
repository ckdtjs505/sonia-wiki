---
url: https://ckdtjs505.github.io/posts/2020-07-22-DevelopmentTip4
layout: post
title: '[Development Tip #4] 매개변수의 기본값을 생성하라'
series: 'Development Tip'
date: 2020-07-22T00:00:00.000Z
author: changsun oh
tags: Tip
comments: true
share: true
related: false
summary: 매개변수 기본값이 필요한 이유와, 기본값으로 기존 코드에 영향 없이 요구사항 변경에 대응하는 방법을 다룹니다.
---

## 목표 
* 매개변수의 기본값의 필요성을 이해한다.
* 매개변수 기본값을 지정하는 방법을 이해한다.  

## 매개변수 기본값 필요성
* 추가되는 요구 사항에 대처시 유용하다.
* 매개변수 기본값을 통해 어떤 자료형인지 유추할수 있다.
* 기존 선언되어 있는 코드에 영향이 없다. 

특정 시간(분) 값을 초로 변환화는 함수를 만들게 되었다. 
그다지 어려워 보일것은 없어 보인다. 시간(분)값을 입력받아 60을 곱해주면 된다. 
  ```javascript
  function convertTimeToSeconds ( minute ){
    return minute * 60;
  }
  console.log( convertTimeToSeconds(2) );
  // 실행결과 
  // 120
  ```

이후에 특정시간에 시각도 포함시켜야 하는 상황이 생긴다면 매개변수 기본값을 생성하여 할당하자.
 ```javascript 
 function convertTimeToSeconds ( minute, hour = 0){
   return minute * 60 + hour * 60 * 60;
 }
 console.log( convertTimeToSeconds(2) );      // 120
 console.log( convertTimeToSeconds(2, 1) );   // 3720
 console.log( convertTimeToSeconds(0, 1) );   // 3600
 ```

만약 매개변수 기본값을 생성하지 않는다면 첫번째 콘솔값은 NaN을 출력하여 정확한 결과값을 확인하기 어렵게 된다. 

