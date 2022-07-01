import json

import datetime
from datetime import datetime as for_strptime

from django.urls import resolve
from django.test import TestCase, Client
from django.http import HttpRequest

from .models import SewerPipe, Rainfall, GuName
from .serializers import SewerPipeModelSerializer, RainfallModelSerializer, GuNameModelSerializer
from .views import RainfallAndSewerPipeInfoApiView

# Create your tests here.
class TestView(TestCase):
    '''
    Assignee : 민지
    '''
    def setUp(self):
        self.client = Client()
        '''샘플 GuName 데이터 생성'''
        self.gu_01 = GuName.objects.create(gubn='01', name='종로구')
        self.gu_02 = GuName.objects.create(gubn='15', name='양천구')
        
        '''샘플 SewerPipe 데이터 생성'''
        self.sewer_pipe_01 = SewerPipe.objects.create(
            idn = '01-0003',
            gubn = self.gu_01,
            gubn_nam = '종로',
            mea_ymd = '2021-12-02 01:12:00',
            mea_wal = 0.11,
            sig_sta = '통신양호',
        )
        self.sewer_pipe_02 = SewerPipe.objects.create(
            idn = '01-0004',
            gubn = self.gu_01,
            gubn_nam = '종로',
            mea_ymd = '2021-12-02 01:12:00',
            mea_wal = 0.12,
            sig_sta = '통신양호',
        )
        self.sewer_pipe_03 = SewerPipe.objects.create(
            idn = '15-0006',
            gubn = self.gu_02,
            gubn_nam = '양천',
            mea_ymd = '2021-12-02 01:12:00',
            mea_wal = 0.12,
            sig_sta = '통신양호',
        )
        self.sewer_pipe_04 = SewerPipe.objects.create(
            idn = '15-0007',
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

    def test_sewer_pipe_model_serializer(self):
        pipe = SewerPipe.objects.filter(gubn='01').first()
        obj = SewerPipeModelSerializer(pipe)
        obj_fields = list(obj.fields)

        self.assertEqual(obj_fields, ['idn', 'mea_wal'])
        
    def test_rainfall_model_serializer(self):
        rainfall = Rainfall.objects.filter(gubn='01').first()
        obj = RainfallModelSerializer(rainfall)
        obj_fields = list(obj.fields)

        self.assertEqual(obj_fields, ['raingauge_name', 'rainfall10'])
    
    def test_gu_name_model_serializer(self):
        gu_obj = GuName.objects.get(gubn='01')
        serialized_gu_obj = GuNameModelSerializer(gu_obj)
        serialized_gu_obj_fields = list(serialized_gu_obj.fields)
        
        self.assertEqual(serialized_gu_obj_fields, ['gubn', 'name', 'rainfall_data', 'sewer_pipe_data'])

    def test_get_rainfall_data_method(self):
        str_datetime_info = '202112020112'
        datetime_info = for_strptime.strptime(str_datetime_info, "%Y%m%d%H%M")

        rainfall_objs = Rainfall.objects.filter(
            gubn='01',
            receive_time__gte=datetime_info,
            receive_time__lt=datetime_info + datetime.timedelta(minutes=10)
            )

        self.assertEqual(rainfall_objs[0].raingauge_name, '종로구청')
        self.assertEqual(rainfall_objs[0].rainfall10, 0.0)
        self.assertEqual(rainfall_objs[1].raingauge_name, '부암동')
        self.assertEqual(rainfall_objs[1].rainfall10, 0.0)
    
    def test_get_sewer_pipe_data_method(self):
        str_datetime_info = '202112020112'
        datetime_info = for_strptime.strptime(str_datetime_info, "%Y%m%d%H%M")

        sewer_pipe_objs = SewerPipe.objects.filter(
            gubn='01',
            mea_ymd__gte=datetime_info,
            mea_ymd__lt=datetime_info + datetime.timedelta(minutes=1)
            )

        self.assertEqual(sewer_pipe_objs[0].idn, '01-0003')
        self.assertEqual(sewer_pipe_objs[0].mea_wal, 0.11)
        self.assertEqual(sewer_pipe_objs[1].idn, '01-0004')
        self.assertEqual(sewer_pipe_objs[1].mea_wal, 0.12)
    
    def test_url_resolves_to_rain_fall_and_sewer_pipe_api_view(self):
        found = resolve('/api/data/v1/rainfall-and-drainpipe-info/<gubn>/<datetime_info>/')

        self.assertEqual(found.func.__name__, RainfallAndSewerPipeInfoApiView.as_view().__name__)

    def test_rain_fall_and_sewer_pipe_api_view_get_guname_object_method(self):
        obj = RainfallAndSewerPipeInfoApiView.get_guname_object(self, '01')
        obj_not_exsist = RainfallAndSewerPipeInfoApiView.get_guname_object(self, '20')

        self.assertEqual(obj.name, '종로구')
        self.assertEqual(obj_not_exsist, None)

    def test_rain_fall_and_sewer_pipe_api_view_get_method(self):
        response = self.client.get('/api/data/v1/rainfall-and-drainpipe-info/01/202112020112/')
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response_json['name'], '양천구')
        self.assertEqual(len(response_json['rainfall_data']), 2)
        self.assertEqual(len(response_json['sewer_pipe_data']), 2)