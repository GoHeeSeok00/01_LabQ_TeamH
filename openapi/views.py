from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import save_sewerpipe_data_all_gubn, save_rainfall_data


# url : openapi/data/save-previous-sewerpipe-data/<start_date>/<end_date>/
class OpenAPISewerPipeSaveApiView(APIView):
    """
    Assignee : 훈희

    Http method = GET only

    날짜를 입력 받아 OpenAPI의 SewerPipe 값을 가져와서 저장하는 API입니다.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, start_date, end_date):
        start_date = int(start_date)
        end_date = int(end_date)
        save_sewerpipe_data_all_gubn(start_date, end_date)

        return Response({f'{start_date} 부터 {end_date}까지 저장하였습니다.'}, status=status.HTTP_200_OK)


# url : openapi/data/save-previous-rainfall-data/<start_date>/<end_date>/
class OpenAPIRainfallSaveApiView(APIView):
    """
    Assignee : 훈희

    Http method = GET only

    날짜를 입력 받아 OpenAPI의 Rainfall 값을 가져와서 저장하는 API입니다.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, start, end):
        start = int(start)
        end = int(end)
        save_rainfall_data(start, end)

        return Response({f'{start} 부터 {end}까지 저장하였습니다.'}, status=status.HTTP_200_OK)
