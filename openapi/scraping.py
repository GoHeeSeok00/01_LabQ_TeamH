from utils import save_rainfall_data, auto_save_sewerpipe_per_10
from datetime import datetime

now = datetime.now()
''' print(now_str) 2022-07-01 17:46:11 '''
now_str = now.strftime('%Y%m%d%H%M')

''' 
    Assignee : 훈희
    
    마지막 시간에서 1을 뺀 값으로 범위를 설정하지만 각 하수관 마다 10개씩만 데이터를 가져오므로 최대 10분의 데이터만 가져온다.
    데이터가 연속적으로 무조건 있으면 최신 업데이트 순으로 10분치의 내용을 추가한다고 이야기 하겠지만 중간중간 
    비어있는 값이 있어서 위와 같이 표현

'''
end_hour = int(now_str)

start_hour = end_hour - 1
auto_save_sewerpipe_per_10(start_hour, end_hour)
''' 10분 마다 47개씩 저장하면 10분마다 저장되는 내용을 다 가져올 수 있음'''
save_rainfall_data(1, 47)
