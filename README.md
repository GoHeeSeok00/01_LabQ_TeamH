# 원티드 프리온보딩 LabQ 기업과제 Team H

<br>

## 👩‍💻 Team
- [고희석](https://github.com/GoHeeSeok00)
- [김훈희](https://github.com/nmdkims)
- [김민지](https://github.com/my970524)
- [이정석](https://github.com/sxxk2)
- [김상백](https://github.com/tkdqor)

- **[Team-H-노션](https://www.notion.so/pre-onboarding-3rd-team-H-03162526802541328690696ec4588fdd)**

<br>

<img src="https://img.shields.io/badge/프로젝트 진행 기간 2022.06.28 ~ 2022.07.01-D3D3D3?style=for-the-badge">

<br>

## 🛠 기술 스택

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">

<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">

<br>

## :ballot_box_with_check: 서비스 개요
- 서울시 지역구별 강우량 및 하수관로 수위 데이터 제공을 통해 데이터 간 위험도 분석, ML학습 등을 위한 기초 데이터를 제공하는 서비스입니다.
- 일반 사용자가 보기 쉽게 기후정보와 하수관로 수위 위험도의 텍스트 표현을 추가했습니다.


<br>

## 📌 과제 분석
- **과제 : Open API 방식의 공공데이터를 수집, 가공하여 전달하는 REST API와 이를 요청하는 클라이언트 개발**

- **데이터**
  - [서울시 하수관로 수위 현황](https://data.seoul.go.kr/dataList/OA-2527/S/1/datasetView.do)
  - [서울시 강우량 정보](http://data.seoul.go.kr/dataList/OA-1168/S/1/datasetView.do)

- **개발요건**
  - **REST API 기능**
    - 서울시 하수관로 수위 현황과 강우량 정보 데이터를 수집
    - 출력값 중 GUBN_NAM과 GU_NAME 기준으로 데이터를 결합
    - 데이터는 JSON으로 전달
  
  - **클라이언트 기능**
    - GUBN(구분코드)를 명시해서 REST API를 호출할 수 있음
    - 서버에서 전송받은 결과를 출력

- **분석결과**


<br>


## 🛠 DB Modeling
![Untitled](https://user-images.githubusercontent.com/95380638/176635745-467ca0d2-c75f-44b5-9607-28202a1dd657.png)
- **SewerPipe 모델** : 서울시 하수관로 수위 현황 데이터 저장 
- **Rainfall 모델** : 서울시 강우량 정보 데이터 저장
- **GuName 모델** : GUBN(구분코드)와 해당하는 서울시 자치구 이름 저장, SewerPipe 및 Rainfall 모델과 각각 1:N 관계 설정


<br>

## 📑 API 명세서

| URL | Method | 논리적 이름 | 물리적 이름 | Permission | 기능 |
| --- | --- | --- | --- | --- | --- |
| /api/data/v1/rainfall-and-drainpipe-info/<gubn>/<datetime_info>/ | `GET` | 강우량 및 하수관로 정보 | rainfall_and_sewerpipe_info | Allow |지역구 코드와 날짜와 시간 정보를 요청인자로 요청받으면 지역구별 강우량, 하수관로 수위 데이터를 응답 |

- **URL 설정 의도** : 서비스의 기획 의도와 맞게 gubn, datetime_info 요청인자를 옵셔널 하게 사용하는게 아니라 요청인자를 리소스로 식별하기 위해 Path Variable로 URL을 설정했습니다.


<br>


### 요청인자

| 변수명 | 타입 | 변수설명 | 값설명 |
| --- | --- | --- | --- |
| `gubn` | String(필수) | 지역구 코드 | 01 ~ 25 (한자리 수는 앞에 0을 붙여 2자리로 만들어줘야 합니다) |
| `datetime_info` | String(필수) | 측정일자 | YYYYMMDDHHmm (연월일시분) |


<br>


### 출력값

| 출력명 | 출력설명 |
| --- | --- |
| `gubn` | 지역구 식별 코드 |
| `name` | 지역구 이름 |
| `rainfall_data` | 강우량 데이터 (json) |
| `raingauge_name` | 강우량계명 |
| `rainfall10` | 10분 우량 정보 |
| `sewer_pipe_data` | 하수관로 데이터(json) |
| `idn` | 하수관로 식별 코드 |
| `mea_wal` | 하수관로 수위 |
| `alert_result` | 강우량, 하수관로 수위에 따른 정보 |


<br>


`alert_result` 추가정보

- 10분 강우량
    - 5이상 : 강우(천둥, 번개 동반)
    - 2.5 이상 : 강우
    - 1.5 이상 : 많은 비
    - 0.5 이상 : 소나기
    - 0.1 이상 : 구름 조금
    - 맑음
- 하수관로 (하수관로 수위를 박스 높이로 나눈 비율)
    - 90% 이상 : 비상
    - 50% 이상 : 위험
    - 안전


<br>


## 🎈 서비스 API 결과 (로컬환경)
![team_h_01_api_result](https://user-images.githubusercontent.com/96563183/176873896-2dabc19a-6e79-4cb9-9fe9-1a978fd6be83.png)
