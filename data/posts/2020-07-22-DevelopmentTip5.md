---
url: https://ckdtjs505.github.io/posts/2020-07-22-DevelopmentTip5
layout: post
title: '[Development Tip #5] 구조 분해 할당'
series: 'Development Tip'
date: 2020-07-22T00:00:00.000Z
author: changsun oh
tags: Tip
comments: true
share: true
related: false
summary: 구조 분해 할당의 개념과 필요성, 그리고 구조 분해 할당으로 코드를 리팩터링한 사례를 정리합니다.
---

## 목표 
* 구조 분해 할당이 무엇인지 이해한다. 
* 구조 분해 할당의 필요성을 이해한다.
* 구조 분해 할당을 이용해 코드를 리팩토링한다.

## 구조 분해 할당이란? 
* 구조 분해 할당은 배열, 객체의 속성을 해채하여 그 값을 개별 변수에 담는다.  

```javascript 
let o = {p:42, q:true};
const { p, q} = o;
console.log( o, p, q);
```

## 구조 분해 할당의 필요성 
* 변수를 선언하지 않고도 할당한것처럼 사용할 수 있다. 

## 구조 분해 할당을 이용 한 사례 
```json
{
    "list": [
        {
            "_returnType": "json",
            "coGrade": "1",
            "coValue": "0.4",
            "dataTime": "2020-09-12 21:00",
            "khaiGrade": "1",
            "khaiValue": "40",
            "mangName": "도시대기",
            "no2Grade": "1",
            "no2Value": "0.005",
            "numOfRows": "10",
            "o3Grade": "1",
            "o3Value": "0.024",
            "pageNo": "1",
            "pm10Grade": "1",
            "pm10Grade1h": "1",
            "pm10Value": "7",
            "pm10Value24": "9",
            "pm25Grade": "1",
            "pm25Grade1h": "1",
            "pm25Value": "3",
            "pm25Value24": "5",
            "rnum": 0,
            "so2Grade": "1",
            "so2Value": "0.002",
        },
    ]
}
```
대기질 정보를 받아온 데이터이다.  구조 분해를 할당하지 않았을 때
```javascript 
function displayAirData(airData){
    const pm10Grade = airData.pm10Grade;
    const pm10Value = airData.pm10Value;
    const pm25Grade = airData.pm25Grade;
    const pm25Value = airData.pm25Value;
    const so2Value = airData.so2Value;
    const o3Value = airData.o3Value;
    const coGrade = airDtat.coGrade;

    return (`
        <div> pm10Grade = ${pm10Grade} <div> 
        <div> pm10Value = ${pm10Value} <div> 
        <div> pm25Grade = ${pm25Grade} <div> 
        <div> pm25Value = ${pm25Value} <div> 
        <div> so2Value = ${pm25Value} <div> 
        <div> o3Value = ${o3Value} <div> 
        <div> coGrade = ${coGrade} <div> 
    `)
}

```

구조 분해를 활용하여 리팩토링 했을 때 
```javascript 
function displayAirData(airData){
    const { 
        pm10Grade, 
        pm10Value, 
        pm25Grade, 
        pm25Value, 
        so2Value, 
        o3Value, 
        coGrade 
    } = airData;

    return (`
        <div> pm10Grade = ${pm10Grade} <div> 
        <div> pm10Value = ${pm10Value} <div> 
        <div> pm25Grade = ${pm25Grade} <div> 
        <div> pm25Value = ${pm25Value} <div> 
        <div> so2Value = ${pm25Value} <div> 
        <div> o3Value = ${o3Value} <div> 
        <div> coGrade = ${coGrade} <div> 
    `)
}
```

