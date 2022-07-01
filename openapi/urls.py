from django.urls import path

from .views import OpenAPISewerPipeSaveApiView, OpenAPIRainfallSaveApiView

app_name = "openapi"

urlpatterns = [
    path('data/save-previous-sewerpipe-data/<start_date>/<end_date>/',
         OpenAPISewerPipeSaveApiView.as_view(), name='save_previous_sewerpipe_data'),
    path('data/save-previous-rainfall-data/<start>/<end>/',
         OpenAPIRainfallSaveApiView.as_view(), name='save_previous_rainfall_data'),
]