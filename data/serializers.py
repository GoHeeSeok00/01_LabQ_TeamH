import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import SewerPipe, Rainfall, GuName


class SewerPipeModelSerializer(ModelSerializer):
    '''
    Assignee : 민지, 상백

    데이터 출력 예시와 동일하게 고유번호, 측정 수위 필드만 출력

    추가로 하수관로 수위 기준을 정하고 수위값에 따라 상태를 응답해주려고 했으나, 
    수위계 박스높이 대비 현재수위를 계산한 수위비율을 비교해야 하므로 해당 로직을 주석처리
    '''     
    
    '''
    alert_result = serializers.SerializerMethodField()
    def get_alert_result(self, obj):
        if obj.mea_wal >= 0.1:
            return "높음"
        elif obj.mea_wal >= 0.05:
            return "보통"
        else:
            return "안전"
    '''        
    
    class Meta:
        model = SewerPipe
        fields = ['idn', 'mea_wal']


class RainfallModelSerializer(ModelSerializer):
    '''
    Assignee : 민지, 상백
    
    데이터 출력 예시와 동일하게 강우량계명, 10분우량 필드만 출력

    추가로 alert_result 필드를 생성해서 get_alert_result 메소드를 호출했을 때,
    rainfall10 필드값에 따라 강우량 기준을 정해서 강우량 상태값을 응답해주는 로직 구성
    '''
    alert_result = serializers.SerializerMethodField()
    def get_alert_result(self, obj):
        if obj.rainfall10 >= 5:
            return "강우(천둥, 번개 동반)"
        elif obj.rainfall10 >= 2.5:
            return "강우"
        elif obj.rainfall10 >= 1.5:
            return "많은 비"
        elif obj.rainfall10 >= 0.5:
            return "소나기"
        elif 0.1 <= obj.rainfall10 <= 0.4:
            return "구름 조금"
        else:
            return "맑음" 
    class Meta:
        model = Rainfall
        fields = ['raingauge_name', 'rainfall10', 'alert_result'] 


class GuNameModelSerializer(ModelSerializer):
    """
    Assignee : 희석

    View단에서 GuName 테이블의 오브젝트가 주어졌을 때
    역참조를 통해 Rainfall, SewerPipe 모델의 쿼리셋을 가져오고
    datetime_info로 필터하여 serializer data 전달
    """
    rainfall_data = serializers.SerializerMethodField()
    sewer_pipe_data = serializers.SerializerMethodField()

    def get_rainfall_data(self, obj):
        rainfalls = obj.rainfall
        datetime_info = self.context["datetime"]
        rainfall_serializer = RainfallModelSerializer(rainfalls.filter(
            receive_time__gte=datetime_info,
            receive_time__lt=datetime_info + datetime.timedelta(minutes=10)
        ), many=True)
        return rainfall_serializer.data

    def get_sewer_pipe_data(self, obj):
        sewer_pipe = obj.sewer_pipe
        datetime_info = self.context["datetime"]
        sewer_pipe_serializer = SewerPipeModelSerializer(sewer_pipe.filter(
            mea_ymd__gte=datetime_info,
            mea_ymd__lt=datetime_info + datetime.timedelta(minutes=1)
        ), many=True)
        return sewer_pipe_serializer.data

    class Meta:
        model = GuName
        fields = ["gubn", "name", "rainfall_data", "sewer_pipe_data"]

