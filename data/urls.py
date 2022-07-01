from django.urls import path

from data.views import RainfallAndSewerPipeInfoApiView

app_name = "data"

urlpatterns = [
    path('api/data/v1/rainfall-and-drainpipe-info/<gubn>/<datetime_info>/',
         RainfallAndSewerPipeInfoApiView.as_view(), name='rainfall_and_sewerpipe_info'),
]