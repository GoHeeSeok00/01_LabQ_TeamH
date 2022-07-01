from datetime import datetime

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models import GuName as GuNameModel
from data.serializers import GuNameModelSerializer

""""""
# Create your views here.

# url : api/data/v1/rainfall-and-drainpipe-info/<gubn>/<datetime_info>/
class RainfallAndSewerPipeInfoApiView(APIView):
    """
    Assignee : 희석

    Http method = GET only

    클라이언트의 요청을 받아 하수관로 및 강우량 정보를
    response 하는 API입니다.
    """
    permission_classes = [permissions.AllowAny]
    def get_guname_object(self, obj_pk):
        try:
            object = GuNameModel.objects.get(gubn=obj_pk)
        except GuNameModel.DoesNotExist:
            """seom event : 찾는 object 없으면 빈값을 return"""
            return
        return object

    def get(self, request, gubn, datetime_info):
        gu_name = self.get_guname_object(gubn)
        """예외처리 : 테이블에 저장되어 있지 않은 오브젝트를 참조할 때"""
        if not gu_name:
            return Response({"error": "gubn 값을 확인해주세요. gubn = 01~25"}, status=status.HTTP_400_BAD_REQUEST)

        """예외처리 : datetime_info의 입력값이 다를 떄"""
        if len(datetime_info) != 12:
            return Response({"error": "datetime_info 값을 확인해주세요. datetime_info = YYYYMMDDHHmm"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            str_to_datetime = datetime.strptime(datetime_info, "%Y%m%d%H%M")
        except ValueError:
            return Response({"error": "datetime_info 값을 확인해주세요. datetime_info = YYYYMMDDHHmm"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(GuNameModelSerializer(gu_name, context={"datetime": str_to_datetime}).data,
                        status=status.HTTP_200_OK)
