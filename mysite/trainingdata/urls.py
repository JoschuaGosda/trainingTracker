from django.urls import path
from django.conf.urls import url
from django.views.generic.dates import ArchiveIndexView
from . import views
from .models import Deadhang_max, Training

urlpatterns = [

    path('deadhang/maximum_strength/create/', views.create_deadhang_max, name='deadhang_max'),
    path('deadhang/maximum_strength/update/<int:pk>', views.DeadhangMaxUpdateView.as_view(), name='update_dmax'),
    #path('deadhang/maximum_strength/update/<int:pk>', views.DeadhangMaxDetailView.as_view(), name='detail_dmax'),
    #path('deadhang/maximum_strength/delete/<int:pk>', views.DeadhangMaxDeleteView.as_view(), name='delete_dmax'),

    path('deadhang/maximum_strength/archive/',
         ArchiveIndexView.as_view(model=Deadhang_max, date_field="date"),
         name="dmax_archive"),

    path('deadhang/strength_endurance/create/', views.create_deadhang_endurance, name='deadhang_endurance'),
    path('deadhang/strength_endurance/update/<int:pk>', views.DeadhangEndUpdateView.as_view(), name='update_dend'),
    #path('deadhang/strength_endurance/<int:pk>', views.DeadhangEndDetailView.as_view(), name='detail_dend'),


    path('pullups/strength_endurance/create/', views.create_pullup_endurance, name='pullup_endurance'),
    path('pullups/strength_endurance/update/<int:pk>', views.PullupEndUpdateView.as_view(), name='update_pend'),
    #path('pullups/strength_endurance/<int:pk>', views.PullupEndDetailView.as_view(), name='detail_pend'),

    path('pullups/maximum_strength/create/', views.create_pullup_max, name='pullup_max'),
    path('pullups/maximum_strength/update/<int:pk>', views.PullupMaxUpdateView.as_view(), name='update_pmax'),
    #path('pullups/maximum_strength/<int:pk>', views.PullupMaxDetailView.as_view(), name='detail_pmax'),


    path('record/', views.RecordListView.as_view(), name='record_list'),
    path('record/max', views.RecordListView_Max.as_view(), name='record_list_max'),
    path('record/end', views.RecordListView_End.as_view(), name='record_list_end'),
    path('record/delete/<int:pk>', views.TrainingDeleteView.as_view(), name='record_list_delete'),
    # path('archive/',
    #      ArchiveIndexView.as_view(model=Training, date_field="date"),
    #      name="deadhang_max_archive"),
     #url(r'^(?P<id>\d+)/$', views.TrainingDmaxView.as_view(), name='detail_dmax'),

     path('custom_training/create/', views.create_custom_training, name='custom_training'),
     path('custom_training/update/<int:pk>', views.CustomTrainingUpdateView.as_view(), name='update_custom_training'),

]
