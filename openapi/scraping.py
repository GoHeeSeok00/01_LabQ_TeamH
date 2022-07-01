from utils import save_rainfall_data, auto_save_sewerpipe_per_10
from datetime import datetime

now = datetime.now()
# print(now)

now_str = now.strftime('%Y-%m-%d %H:%M:%S')
# print(now_str) 2022-07-01 17:46:11

end_date = int(
    now_str[0] + now_str[1] + now_str[2] + now_str[3] + now_str[5] + now_str[6] + now_str[8] + now_str[9] + now_str[
        11] + now_str[12])

start_data = end_date-1
print(end_date)
print(start_data)
auto_save_sewerpipe_per_10(start_data, start_data)
''' 10분 마다 47개씩 저장하면 10분마다 저장되는 내용을 다 가져올 수 있음'''
# save_rainfall_data(1, 47)
# save_rainfall_data()
# save_sewerpipe_data_all_gubn()
