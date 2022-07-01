from rest_framework.serializers import ModelSerializer
from data.models import SewerPipe


class OpenAPISewerPipeModelSerializer(ModelSerializer):
    '''
    Assignee : 훈희

    기본 형태 작성
    '''

    class Meta:
        model = SewerPipe
        fields = [
            'idn',
            'gubn',
            'gubn_nam',
            'mea_ymd',
            'mea_wal',
            'sig_sta'
        ]
