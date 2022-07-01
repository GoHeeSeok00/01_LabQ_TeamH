import json

from django.test import TestCase, Client
from django.urls import resolve

from ..models import SewerPipe, Rainfall, GuName, SewerPipeBoxInfo
from ..views import RainfallAndSewerPipeInfoApiView

class ViewTestCase(TestCase):
    '''
    Assignee : 민지

    뷰, 뷰의 메소드를 테스트합니다.
    총 3개의 테스트 케이스가 있습니다.
    '''

    def setUp(self):
        '''Test를 위한 데이터 생성 및 셋팅'''

        self.client = Client()

        '''샘플 GuName 데이터 생성'''
        self.gu_01 = GuName.objects.create(gubn='01', name='종로구')
        self.gu_02 = GuName.objects.create(gubn='15', name='양천구')
        
        '''샘플 SewerPipeBoxInfo 데이터 생성'''
        self.sewer_pipe_box_info_01 = SewerPipeBoxInfo.objects.create(
            idn = '01-0003',
            box_height = 2.1,
        )
        self.sewer_pipe_box_info_02 = SewerPipeBoxInfo.objects.create(
            idn = '01-0004',
            box_height = 1.8,
        )
        self.sewer_pipe_box_info_03 = SewerPipeBoxInfo.objects.create(
            idn = '15-0006',
            box_height = 2.6,
        )
        self.sewer_pipe_box_info_04 = SewerPipeBoxInfo.objects.create(
            idn = '15-0007',
            box_height = 2.4,
        )

        '''샘플 SewerPipe 데이터 생성'''
        self.sewer_pipe_01 = SewerPipe.objects.create(
            idn = self.sewer_pipe_box_info_01,
            gubn = self.gu_01,
            gubn_nam = '종로',
            mea_ymd = '2021-12-02 01:12:00',
            mea_wal = 0.11,
            sig_sta = '통신양호',
        )
        self.sewer_pipe_02 = SewerPipe.objects.create(
            idn = self.sewer_pipe_box_info_02,
            gubn = self.gu_01,
            gubn_nam = '종로',
            mea_ymd = '2021-12-02 01:12:00',
            mea_wal = 0.12,
            sig_sta = '통신양호',
        )
        self.sewer_pipe_03 = SewerPipe.objects.create(
            idn = self.sewer_pipe_box_info_03,
            gubn = self.gu_02,
            gubn_nam = '양천',
            mea_ymd = '2021-12-02 01:12:00',
            mea_wal = 0.12,
            sig_sta = '통신양호',
        )
        self.sewer_pipe_04 = SewerPipe.objects.create(
            idn = self.sewer_pipe_box_info_04,
            gubn = self.gu_02,
            gubn_nam = '양천',
            mea_ymd = '2021-12-02 01:12:00',
            mea_wal = 0.0,
            sig_sta = '통신양호'
        )
        '''샘플 Rainfall 데이터 생성'''
        self.rainfall_01 = Rainfall.objects.create(
            raingauge_code = '1001',
            raingauge_name = '종로구청',
            gu_code = 110,
            gu_name = '종로구',
            rainfall10 = 0.0,
            receive_time = '2021-12-02 01:19',
            gubn = self.gu_01
        )
        self.rainfall_02 = Rainfall.objects.create(
            raingauge_code = '1002',
            raingauge_name = '부암동',
            gu_code = 110,
            gu_name = '종로구',
            rainfall10 = 0.0,
            receive_time = '2021-12-02 01:19',
            gubn = self.gu_01
        )
        self.rainfall_03 = Rainfall.objects.create(
            raingauge_code = '1801',
            raingauge_name = '양천구청',
            gu_code = 118,
            gu_name = '양천구',
            rainfall10 = 0.0,
            receive_time = '2021-12-02 01:19',
            gubn = self.gu_02
        )
        self.rainfall_04 = Rainfall.objects.create(
            raingauge_code = '1802',
            raingauge_name = '양천구청',
            gu_code = 118,
            gu_name = '양천구',
            rainfall10 = 0.0,
            receive_time = '2021-12-02 01:19',
            gubn = self.gu_02
        )
    
    def test_url_resolves_to_rain_fall_and_sewer_pipe_api_view(self):
        '''url과 view가 잘 매치되었는지 Test'''

        found = resolve('/api/data/v1/rainfall-and-sewerpipe-info/<gubn>/<datetime_info>/')

        self.assertEqual(found.func.__name__, RainfallAndSewerPipeInfoApiView.as_view().__name__)

    def test_rain_fall_and_sewer_pipe_api_view_get_guname_object_method(self):
        '''RainfallAndSewerPipeInfoApiView의 get_guname_object 메소드 Test'''

        obj = RainfallAndSewerPipeInfoApiView.get_guname_object(self, '01')
        obj_not_exsist = RainfallAndSewerPipeInfoApiView.get_guname_object(self, '20')

        self.assertEqual(obj.name, '종로구')
        self.assertEqual(obj_not_exsist, None)

    def test_rain_fall_and_sewer_pipe_api_view_get_method(self):
        '''RainfallAndSewerPipeInfoApiView으로 GET 요청 TEST'''

        response = self.client.get('/api/data/v1/rainfall-and-sewerpipe-info/01/202112020112/')
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response_json['name'], '양천구')
        self.assertEqual(len(response_json['rainfall_data']), 2)
        self.assertEqual(len(response_json['sewer_pipe_data']), 2)