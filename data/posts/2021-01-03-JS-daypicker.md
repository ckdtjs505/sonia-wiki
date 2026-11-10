---
url: https://ckdtjs505.github.io/posts/2021-01-03-JS-daypicker
layout: post
title: '[js] js-datepicker 사용하기'
date: 2021-01-03T00:00:00.000Z
tags: javascript
comments: true
share: true
related: false
summary: 자바스크립트 Datepicker 라이브러리 활용법과 날짜 선택 컴포넌트 구현 방법을 다룹니다.
---


### 목표
* 어드민 페이지에서 시작일을 설정 할 수 있어야함  
* 입력 날자 형식을 맞춰 줄 수 있는 `js-datepicker`를 사용 

### 이유
* 입력 날자 형식을 맞추고자 
* 날자 입력시 사용자가 간편하게 입력하고자 
* `js-datepicker`의 크기는 5.9kb이면서 `종속성`을 가지고 있지 않고
* 문서 설명이 잘되어 있음. [https://www.npmjs.com/package/js-datepicker#formatter]

### 내용 
1. js-datepicker 설치 
```
 npm install js-datepicker
```

2. js-datepicker 설정
```js
main.js

...

    // datePicker
    this.startDatePicker = datepicker("#inputStartDate", {
      // 시작일 입력 달력
      showAllDates: true,
      // 월 설정 
      customMonths: [
        "1월",
        "2월",
        "3월",
        "4월",
        "5월",
        "6월",
        "7월",
        "8월",
        "9월",
        "10월 ",
        "11월 ",
        "12월 "
      ],
      // 형식 설정 
      formatter: (input, date, instance) => {
        const value = date.toLocaleDateString();
        input.value = value; // => '1/1/2099'
      }
    });

    // 이벤트 설정 
    // input dom 선택시 => show() 
    this.startDateInput.addEventListener("click", () => {
      this.startDatePicker.show();
    });

... 
```

### 결론
* 외부 모듈을 사용하여 간단하게 날자를 입력 해 보았다. 
* js-datepicker를 원하는 형식으로 변경 해 보았다. 
