# 원티드 프리온보딩 LabQ 기업과제 Team H


<br>


## ‼ 배포 서비스 종료
AWS EC2, RDS를 이용해 배포하고 자동화 로직을 구현했으나 10분마다 OpenApi에 요청하여 데이터를 저장하는 데서 비용의 부담이 발생해 서비스를 종료했습니다. 자세한 배포 과정과 서비스 내용은 아래 캡쳐 화면으로 확인할 수 있습니다.


<br>


## 👩‍💻 Team H
- [고희석](https://github.com/GoHeeSeok00)
- [김훈희](https://github.com/nmdkims)
- [김민지](https://github.com/my970524)
- [이정석](https://github.com/sxxk2)
- [김상백](https://github.com/tkdqor)

- **[Team-H-노션](https://www.notion.so/a540c56f257746f08d185ac04d3db11c)**

<br>

<img src="https://img.shields.io/badge/프로젝트 진행 기간 2022.06.28 ~ 2022.07.01-D3D3D3?style=for-the-badge">

<br>

## 🛠 사용 기술

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">

<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">

<img src="https://img.shields.io/badge/aws-232F3E?style=for-the-badge&logo=aws&logoColor=white">

<img src="https://img.shields.io/badge/MySQL-232F3E?style=for-the-badge&logo=MySQL&logoColor=white">

<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white">

<img src="https://img.shields.io/badge/Github Actions-000000?style=for-the-badge&logo=Github Actions&logoColor=white">


<br>

## :ballot_box_with_check: 서비스 개요
- 서울시 지역구별 강우량 및 하수관로 수위 데이터 제공을 통해 데이터 간 위험도 분석, ML학습 등을 위한 기초 데이터를 제공하는 서비스입니다.
- 일반 사용자가 보기 쉽게 기후정보와 하수관로 수위 위험도의 텍스트 표현을 추가했습니다.


<br>

## 📌 과제 분석

### 과제 내용

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

### 분석
- **목표 : Open API 방식의 공공데이터를 수집, 가공하여 전달하는 REST API와 이를 요청하는 클라이언트 개발**

서울시 강우량과 하수관로 데이터는 공공 api를 통해 얻을 수 있다. 우리 서버는 이 데이터를 요구사항에 맞게 전처리하여 응답으로 보내주면 된다.

❗️ 강우량 데이터와 하수관로 데이터셋은 각각 다른 이름으로 ‘지역구'를 지정한다. 

➡️ 두 데이터셋을 ‘지역구'로 결합하기 위해 관계를 이어줄 수 있는 테이블을 생성한다. 

❗️ 클라이언트가 우리 서비스의 rest api를 요청할 때마다 공공 api를 호출하게 설계하는 경우, 공공 api 서버에 문제가 생기면 우리 서비스의 서버도 작동하지 못하게 된다. 

➡️ DB에 데이터셋을 넣어놓고, 요청에 맞는 데이터를 DB에서 조회하여 제공해준다. 

❗️ DB에는 과거의 데이터셋만 넣어놨기 때문에, 클라이언트가 최신 데이터를 요청하는 경우 응답할 수 없다.

➡️ 일정 간격으로 DB 최신화하는 작업을 자동화 한다.

❗️ 강우량 데이터와 하수관로 데이터의 측정시간 다르다. 강우량 데이터는 10분 단위로 기록, 하수관로 데이터는 1분단위로 기록

➡️ ex) 클라이언트가 ‘마포구’의 ‘2021년 11월 1일 23시 50분'데이터를 요청할 경우

➡️ 강우량 테이블에서는 ‘마포구'의 ‘2021년 11월 1일 23시 59분’ 기록을 보여주고, 하수관로 테이블에서는 ‘2021년 11월 1일 23시 50분’의 모든 하수관 데이터를 보여준다.

➡️ 두 데이터의 시간 기준을 잡아서(ex: 기상청 업데이트 기준과 동일한 30분 단위) 데이터를 정제하여 보여준다. 

(이 때, 시간 기준을 잡은 이유에 대한 부분은 논리적으로 설명 가능해야 한다.)


<br>


## 로컬에서 실행하기

```
1. 로컬에 파이썬 3.9 버전과 pipenv 설치
2. git clone
3. clone한 프로젝트 폴더경로에서 `pipenv install` 명령어 실행
4. `pipenv shell`명령어로 가상환경 접속
```

<br>


## 🛠 DB Modeling
![랩큐_ERD_하수관 정보 테이블 추가](https://user-images.githubusercontent.com/96563183/176884532-b78ac91b-9395-4a62-a8b0-54fb9cc431a5.png)
- **SewerPipe 모델** : 서울시 하수관로 수위 현황 데이터 저장 
- **SewerPipeBoxInfo 모델** : IDN(하수관로 식별 코드)와 박스 높이 저장, SewerPipe와 1:N 관계 
- **Rainfall 모델** : 서울시 강우량 정보 데이터 저장
- **GuName 모델** : GUBN(구분코드)와 해당하는 서울시 자치구 이름 저장, SewerPipe 및 Rainfall 모델과 각각 1:N 관계 설정


<br>

## 📑 API 명세서

| URL | Method | 논리적 이름 | 물리적 이름 | Permission | 기능 |
| --- | --- | --- | --- | --- | --- |
| /api/data/v1/rainfall-and-sewerpipe-info/\<gubn>/<datetime_info>/ | `GET` | 강우량 및 하수관로 정보 | rainfall_and_sewerpipe_info | AllowAny |지역구 코드와 날짜와 시간 정보를 요청인자로 요청받으면 지역구별 강우량, 하수관로 수위 데이터를 응답 |
| /openapi/data/save-previous-sewerpipe-data/<start_date>/<end_date>/ | `GET` | 하수관로 데이터 요청 및 저장 | save-previous-sewerpipe-data | IsAdminUser | open api에 요청을 보내서 하수관로 데이터를 받고 저장 |
| /openapi/data/save-previous-rainfall-data/<start_date>/<end_date>/ | `GET` | 강우량 데이터 요청 및 저장 | ave-previous-rainfall-data | IsAdminUser | open api에 요청을 보내서 강우량 데이터를 받고 저장 | 

- **URL 설정 의도** <br>
서비스의 기획 의도와 맞게 gubn, datetime_info 요청인자를 옵셔널 하게 사용하는게 아니라 요청인자를 리소스로 식별하기 위해 Path Variable로 URL을 설정했습니다. open api에 요청을 보낼때도 필수 인자들이기 때문에 Path Variable로 URL을 설정했습니다.


<br>


### 요청인자

| 변수명 | 타입 | 변수설명 | 값설명 |
| --- | --- | --- | --- |
| `gubn` | String(필수) | 지역구 코드 | 01 ~ 25 (한자리 수는 앞에 0을 붙여 2자리로 만들어줘야 합니다) |
| `datetime_info` | String(필수) | 측정일자 | YYYYMMDDHHmm (연월일시분) |
|`start_date` | String(필수) | 요청 데이터의 시작점 | YYYYMMDDHH | 
| `end_date` | String(필수) | 요청 데이터의 끝점 | YYYYMMDDHH |


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


<br>


## 💥 서비스 API 결과 (AWS 환경)
<img width="1920" alt="스크린샷 2022-07-01 오후 10 16 07" src="https://user-images.githubusercontent.com/83942213/176902650-1d0d994b-b09c-46f2-b40d-ab0c95ced59f.png">



<br>


## ⛓ 배포
<img width="466" alt="스크린샷 2022-07-01 오후 4 48 42" src="https://user-images.githubusercontent.com/83942213/176887716-0533284e-c5b9-4d1c-bc1c-6b5f25ce74fd.png">

#### 배포 url: [13.125.119.226:8000/](http://13.125.119.226:8000/) (기본 url은 404)

데이터베이스는 AWS RDS MySQL서버로 배포하였고,<br>
API서버는 AWS EC2로 배포하였습니다. <br>



<br>


## DB 업데이트 자동화
![image](https://user-images.githubusercontent.com/89897944/176912781-24cda841-b09b-4774-a3d6-2a979ab269e8.png)
주기적으로 업데이트 되는 공공 데이터를 자동으로 저장해주는 크롤러를 구현 하였습니다. <br>
보안의 문제로 저장소를 분리시켜두었습니다.

## Git action을 이용하여 일정 시간마다 크롤링하는 모습
![image](https://user-images.githubusercontent.com/89897944/177033190-4748929a-3911-4710-b32b-abd786771336.png)



<br>


## Test Case
- Unittest 
- 장고에서 제공하는 기능 외에 직접 작성한 Serialize, View에 대해 테스트 진행
- 10개의 테스트 케이스 모두 통과
