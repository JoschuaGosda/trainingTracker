from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('analyse/', views.analyse_data, name='analyse_data'),
    url(r'^api/chart/data/dmax/$', views.ChartDataHMAX.as_view()),
    url(r'^api/chart/data/dend/$', views.ChartDataHEND.as_view()),
    url(r'^api/chart/data/pmax/$', views.ChartDataPMAX.as_view()),
    url(r'^api/chart/data/pend/$', views.ChartDataPEND.as_view()),
    path('users/', views.UserList.as_view()),
    path('test/', views.test, name='testchart'),
]
