from labq.my_settings import api_authenticate_key
import requests

import time

''' 장고에 등록 되어있지 않은 곳에서 장고 모델을 참조하기 위한 준비 '''
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labq.settings")
import django

django.setup()

from data.models import Rainfall, SewerPipe, GuName
from labq.my_settings import DATABASES


def init_data(data_table_name):
    '''
    Assignee : 훈희

    테이블을 비워주는 함수 파라미터에 data_table 넣어 삭제
    해당 함수 동작을 위하여 sqlite3,time 모듈을 임포트
    time 딜레이를 주면서 작업이 확실히 되고 지나갈 시간을 줌

    data_table_name : 지울 테이블 이름
    '''
    db = DATABASES
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM {data_table_name};")
    db.commit()
    time.sleep(2)
    db.close()


def create_guname():
    '''
        Assignee : 훈희

        data_guname 필드를 채워주는 함수
        함수 실행시 밑의 guname_list에 작성 된 내용을
        data_guname 테이블에 저장
        해당 함수 실행시 초기화는 일어나지 않기 때문에 데이터 추가용으로 사용 가능
        초기화를 하고 싶으면 위의 초기화 함수를 사용
    '''
    guname_list = [
        {
            'GUBN': '01',
            'GUBN_NAM': '종로'
        },
        {
            'GUBN': '02',
            'GUBN_NAM': '중'
        },
        {
            'GUBN': '03',
            'GUBN_NAM': '용산'
        },
        {
            'GUBN': '04',
            'GUBN_NAM': '성동'
        },
        {
            'GUBN': '05',
            'GUBN_NAM': '광진'
        },
        {
            'GUBN': '06',
            'GUBN_NAM': '동대문'
        },
        {
            'GUBN': '07',
            'GUBN_NAM': '중광'
        },
        {
            'GUBN': '08',
            'GUBN_NAM': '성북'
        },
        {
            'GUBN': '09',
            'GUBN_NAM': '강북'
        },
        {
            'GUBN': '10',
            'GUBN_NAM': '도봉'
        },
        {
            'GUBN': '11',
            'GUBN_NAM': '노원'
        },
        {
            'GUBN': '12',
            'GUBN_NAM': '은평'
        },
        {
            'GUBN': '13',
            'GUBN_NAM': '서대문'
        },
        {
            'GUBN': '14',
            'GUBN_NAM': '마포'
        },
        {
            'GUBN': '15',
            'GUBN_NAM': '양천'
        },
        {
            'GUBN': '16',
            'GUBN_NAM': '강서'
        },
        {
            'GUBN': '17',
            'GUBN_NAM': '구로'
        },
        {
            'GUBN': '18',
            'GUBN_NAM': '금천'
        },
        {
            'GUBN': '19',
            'GUBN_NAM': '영등포'
        },
        {
            'GUBN': '20',
            'GUBN_NAM': '동작'
        },
        {
            'GUBN': '21',
            'GUBN_NAM': '관악'
        },
        {
            'GUBN': '22',
            'GUBN_NAM': '서초'
        },
        {
            'GUBN': '23',
            'GUBN_NAM': '강남'
        },
        {
            'GUBN': '24',
            'GUBN_NAM': '송파'
        },
        {
            'GUBN': '25',
            'GUBN_NAM': '강동'
        },
        {
            'GUBN': '미판별',
            'GUBN_NAM': '미판별'
        }
    ]

    for guname in guname_list:
        gubn = guname['GUBN']
        gubn_nam = guname['GUBN_NAM']
        print(f"GUBN:{gubn}")
        print(f"GUBN:{gubn_nam}")
        GuName(gubn=gubn, name=gubn_nam).save()


def save_rainfall_data(start, end):
    '''
    Assignee : 훈희

    강우량 정보를 공공 api에서 가져와서 저장

    start : 가져올 정보의 시작 점 / end : 가져올 정보의 끝 점
    '''
    url = f"http://openapi.seoul.go.kr:8088/{api_authenticate_key}/json/ListRainfallService/{start}/{end}"
    response = requests.get(url)

    result = response.json()['ListRainfallService']
    print(result['list_total_count'])

    result_second = result['row']
    for rainfall_list in result_second:
        RAINGAUGE_CODE = rainfall_list['RAINGAUGE_CODE']
        RAINGAUGE_NAME = rainfall_list['RAINGAUGE_NAME']
        GU_CODE = rainfall_list['GU_CODE']
        GU_NAME = rainfall_list['GU_NAME']
        RAINFALL10 = rainfall_list['RAINFALL10']
        RECEIVE_TIME = rainfall_list['RECEIVE_TIME']

        if GU_NAME.find("종로") == 0:
            GUBN_ID = '01'
        elif GU_NAME.find("중") == 0:
            GUBN_ID = '02'
        elif GU_NAME.find("용산") == 0:
            GUBN_ID = '03'
        elif GU_NAME.find("성동") == 0:
            GUBN_ID = '04'
        elif GU_NAME.find("광진") == 0:
            GUBN_ID = '05'
        elif GU_NAME.find("동대문") == 0:
            GUBN_ID = '06'
        elif GU_NAME.find("중광") == 0:
            GUBN_ID = '07'
        elif GU_NAME.find("성북") == 0:
            GUBN_ID = '08'
        elif GU_NAME.find("강북") == 0:
            GUBN_ID = '09'
        elif GU_NAME.find("도봉") == 0:
            GUBN_ID = '10'
        elif GU_NAME.find("노원") == 0:
            GUBN_ID = '11'
        elif GU_NAME.find("은평") == 0:
            GUBN_ID = '12'
        elif GU_NAME.find("서대문") == 0:
            GUBN_ID = '13'
        elif GU_NAME.find("마포") == 0:
            GUBN_ID = '14'
        elif GU_NAME.find("양천") == 0:
            GUBN_ID = '15'
        elif GU_NAME.find("강서") == 0:
            GUBN_ID = '16'
        elif GU_NAME.find("구로") == 0:
            GUBN_ID = '17'
        elif GU_NAME.find("금천") == 0:
            GUBN_ID = '18'
        elif GU_NAME.find("영등포") == 0:
            GUBN_ID = '19'
        elif GU_NAME.find("동작") == 0:
            GUBN_ID = '20'
        elif GU_NAME.find("관악") == 0:
            GUBN_ID = '21'
        elif GU_NAME.find("서초") == 0:
            GUBN_ID = '22'
        elif GU_NAME.find("강남") == 0:
            GUBN_ID = '23'
        elif GU_NAME.find("송파") == 0:
            GUBN_ID = '24'
        elif GU_NAME.find("강동") == 0:
            GUBN_ID = '25'
        else:
            GUBN_ID = '미판별'

        print(f"RAINGAUGE_CODE:{RAINGAUGE_CODE}")
        print(f"RAINGAUGE_NAME:{RAINGAUGE_NAME}")
        print(f"GU_CODE:{GU_CODE}")
        print(f"GU_NAME:{GU_NAME}")
        print(f"RAINFALL10:{RAINFALL10}")
        print(f"RECEIVE_TIME:{RECEIVE_TIME}")

        Rainfall(raingauge_code=RAINGAUGE_CODE, raingauge_name=RAINGAUGE_NAME, gu_code=GU_CODE, gu_name=GU_NAME,
                 rainfall10=RAINFALL10, receive_time=RECEIVE_TIME, gubn_id=GUBN_ID).save()


def save_sewerpipe_data(start, end, gubn, start_date, end_date):
    '''
       Assignee : 훈희

       하수관 정보를 공공 api에서 가져와서 저장하는 함수
       처음 변수인 start와 end는 해당 범위에서 몇개의 정보를 가져올지 설정
       start_date와 end_date 가져올 데이터의 날짜 분 단위까지 작성

       start : 가져올 정보의 시작 점 / end : 가져올 정보의 끝 점 / gubn : 구분번호 / start_date : 시작 날짜 / end_date : 끝 날짜
    '''
    url = f"http://openAPI.seoul.go.kr:8088/{api_authenticate_key}/json/DrainpipeMonitoringInfo/{start}/{end}/{gubn}/{start_date}/{end_date}"
    response = requests.get(url)
    try:
        result = response.json()['DrainpipeMonitoringInfo']
        print('===============================')
        print(result)
        print('===============================')
        print(result['list_total_count'])

        result_second = result['row']
        for sewerpipe_list in result_second:
            IDN = sewerpipe_list['IDN']
            GUBN_NAM = sewerpipe_list['GUBN_NAM']
            MEA_YMD = sewerpipe_list['MEA_YMD']
            MEA_WAL = sewerpipe_list['MEA_WAL']
            SIG_STA = sewerpipe_list['SIG_STA']
            GUBN = sewerpipe_list['GUBN']

            print(f"IDN:{IDN}")
            print(f"GUBN_NAM:{GUBN_NAM}")
            print(f"MEA_YMD:{MEA_YMD}")
            print(f"MEA_WAL:{MEA_WAL}")
            print(f"SIG_STA:{SIG_STA}")
            print(f"GUBN:{GUBN}")

            SewerPipe(idn=IDN, gubn_nam=GUBN_NAM, mea_ymd=MEA_YMD, mea_wal=MEA_WAL,
                      sig_sta=SIG_STA, gubn_id=GUBN).save()
    except:
        print("========================================")
        print(f"구분번호 : {gubn}의 내용이 포함되지 않았습니다.")
        print("========================================")
        pass
    else:
        pass


def save_sewerpipe_data_all_gubn(start_date, end_date):
    '''
       Assignee : 훈희

       하수관 정보를 공공 api에서 가져와서 저장하는 함수
       처음 변수인 start와 end는 해당 범위에서 몇개의 정보를 가져올지 설정
       start_date와 end_date 가져올 데이터의 날짜 분 단위까지 작성

       start_date : 가져올 정보의 시작 점 / end_date : 가져올 정보의 끝 점
    '''
    gubn_nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                 '18', '19', '20', '21', '22', '23', '24', '25']
    sewer_pipe_count = [4, 5, 3, 7, 12, 14, 8, 1, 2, 9, 11, 8, 11, 20, 12, 12, 13, 8, 12, 3, 6, 7, 21, 2, 4]

    for i, gubn_num in enumerate(gubn_nums):
        gubn = gubn_num
        total_data_per_hour = (end_date - start_date + 1) * sewer_pipe_count[i] * 60

        ''' save_sewerpipe_previous_data(start, end, gubn, start_date, end_date): 함수 파라미터 확인 '''
        save_sewerpipe_data(1, total_data_per_hour, gubn, start_date, end_date)

def auto_save_sewerpipe_per_10(start_date, end_date):
    '''
       Assignee : 훈희

       하수관 정보를 공공 api에서 가져와서 자동으로 저장하는 함수
       10분 단위로 설정

       start_date : 가져올 정보의 시작 점 / end_date : 가져올 정보의 끝 점
    '''
    gubn_nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                 '18', '19', '20', '21', '22', '23', '24', '25']
    sewer_pipe_count = [4, 5, 3, 7, 12, 14, 8, 1, 2, 9, 11, 8, 11, 20, 12, 12, 13, 8, 12, 3, 6, 7, 21, 2, 4]

    for i, gubn_num in enumerate(gubn_nums):
        gubn = gubn_num
        total_data_per_10 = (end_date - start_date + 1) * sewer_pipe_count[i] * 10

        ''' save_sewerpipe_previous_data(start, end, gubn, start_date, end_date): 함수 파라미터 확인 '''
        save_sewerpipe_data(1, total_data_per_10, gubn, start_date, end_date)
'''
    *** 초기 data_guname 테이블 생성 *** 
    data_guname 초기화 후 생성

    init_data('data_guname')
    create_guname()

    *** 사용 예시 ***    
    init_data('table 이름'): 함수 파라미터 확인  data_rainfall, data_sewerpipe, data_guname 
    init_data('data_rainfall')

    save_rainfall_data(시작 값, 끝 값): 시작 값부터 끝 값까지 값을 불러와서 저장함 시작값은 최신값
    save_rainfall_data(1, 1000)

    save_sewerpipe_data_all_gubn(사작 시간, 끝시간): 년도(4글자)월(2글자)일(2글자)분(2글자) 까지 입력
    save_sewerpipe_data_all_gubn(2022062900, 2022062923)

    save_sewerpipe_data(시작 값, 끝 값, 구분 번호, 사작 시간, 끝시간): 위 함수의 단건 저장 기능 
    구분 번호를 설정하여 해당 구분 번호만 저장 가능
    save_sewerpipe_data(1, 1000, '01', 2022062900, 2022062923)
'''
