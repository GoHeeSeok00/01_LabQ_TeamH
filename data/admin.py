from django.contrib import admin
from .models import SewerPipe, Rainfall, GuName

# Register your models here.

@admin.register(SewerPipe)
class SewerPipeModelAdmin(admin.ModelAdmin):
    '''
    Assignee : 상백

    SewerPipe 모델 어드민 페이지 설정
    '''
    list_display = ('idn', 'gubn', 'gubn_nam', 'mea_ymd', 'mea_wal', 'sig_sta')


@admin.register(Rainfall)
class RainfallModelAdmin(admin.ModelAdmin):
    '''
    Assignee : 상백

    Rainfall 모델 어드민 페이지 설정
    '''
    list_display = ('raingauge_code', 'raingauge_name', 'gu_code', 'gu_name', 'rainfall10', 'receive_time', 'gubn')

@admin.register(GuName)
class GuNameModelAdmin(admin.ModelAdmin):
    '''
    Assignee : 민지

    Guname 모델 어드민 페이지 설정
    '''
    list_display = ('gubn', 'name')