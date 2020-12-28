from django.shortcuts import render
from django.views.generic import View
# Rest rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.request import Request

from trainingdata.models import  Deadhang_max, Deadhang_endurance, Pullup_max, Pullup_endurance, Training, CustomSession, TrainingHistory
from .serializers import DeadhangMaxSerializer, DeadhangEndSerializer, PullupMaxSerializer, PullupEndSerializer
from .serializers import UserSerializer
from users.models import CustomUser
from rest_framework import generics
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Q
import json

def test(request):
    return render(request, 'analyse/testchart.html',{})

def analyse_data(request):
    user = request.user
    if(Deadhang_max.objects.filter(user=user).filter(hands = 'TH').filter(hand_position = 'HG').count() > 0):
        twohands_halfgrimp = True
    else:
        twohands_halfgrimp = False
    if(Deadhang_max.objects.filter(user=user).filter(hands = 'TH').filter(hand_position = 'OH').count() > 0):
        twohands_openhand = True
    else:
        twohands_openhand = False
    if(Deadhang_max.objects.filter(user=user).filter(hands = 'OH').filter(hand_position = 'HG').count() > 0):
        onehand_halfgrimp = True
    else:
        onehand_halfgrimp = False
    if(Deadhang_max.objects.filter(user=user).filter(hands = 'OH').filter(hand_position = 'OH').count() > 0):
        onehand_openhand = True
    else:
        onehand_openhand = False

    ####################################
    if(Deadhang_endurance.objects.filter(user=user).filter(hold_duration="2").filter(hand_position = 'OH').count() > 0):
        long_duration_open = True
    else:
        long_duration_open = False
    if(Deadhang_endurance.objects.filter(user=user).filter(hold_duration="2").filter(hand_position = 'HG').count() > 0):
        long_duration_half = True
    else:
        long_duration_half = False
    #####################################
    if(Deadhang_endurance.objects.filter(user=user).filter(hold_duration="1").filter(hand_position = 'OH').count() > 0):
        short_duration_open = True
    else:
        short_duration_open = False

    if(Deadhang_endurance.objects.filter(user=user).filter(hold_duration="1").filter(hand_position = 'HG').count() > 0):
        short_duration_half = True
    else:
        short_duration_half = False
    ##################################
    if(Pullup_max.objects.filter(user=user).count() > 0):
        pullup_max = True
    else:
        pullup_max = False
    if(Pullup_endurance.objects.filter(user=user).count()):
        pullup_endurance = True
    else:
        pullup_endurance = False

    # Additional added for another diagram
    """ past_weeks = 15
    history_dict = {new_list: [] for new_list in range(past_weeks)} 
    week_dict = dict.fromkeys(['max_finger', 'max_pull', 'max_core','end_finger','end_pull', 'end_core', 'flex', 'antagonist','other'])
    day_offset = datetime.today().weekday()
    # current_date starts at beginning of this week
    current_date = timezone.now().date() - timedelta(days=day_offset)
    print("date", current_date)
    counter=0
    for i in range(past_weeks+1): #loop through weeks
        start_date = current_date - timedelta(days=7*(past_weeks-counter))
        end_date = start_date + timedelta(days=7)
        predefined_weekly_training_objects = Training.objects.filter(date__gte=start_date, date__lt=end_date)
        custom_weekly_training_objects = CustomSession.objects.filter(date__gte=start_date, date__lt=end_date)
        #print(weekly_training_objects)
        #value = start_date.isocalendar()[1]
        counter = counter+1
        week_dict['max_finger'] = predefined_weekly_training_objects.filter(title='d1').count() + custom_weekly_training_objects.filter(Q(target='1') & Q(energy_system='1')).count()
        week_dict['max_pull']   = predefined_weekly_training_objects.filter(title='p1').count()
        week_dict['max_core']   = custom_weekly_training_objects.filter(Q(target='3') & Q(energy_system='1')).count()
        week_dict['end_finger'] = predefined_weekly_training_objects.filter(title='d2').count()
        week_dict['end_pull']   = predefined_weekly_training_objects.filter(title='p2').count()
        week_dict['end_core']   = custom_weekly_training_objects.filter(Q(target='3') & Q(energy_system='2')).count()
        week_dict['flex']       = custom_weekly_training_objects.filter(target='4').count()
        week_dict['antagonist'] = custom_weekly_training_objects.filter(target='5').count()
        week_dict['other']      = custom_weekly_training_objects.filter(target='6').count()
        #print("week_dict",week_dict)
        history_dict[i] = week_dict
    print("history_dict", history_dict)
    print("startdate", start_date)
    print("endate", end_date)
    print("test_validation", predefined_weekly_training_objects.filter(title='d1').count() + custom_weekly_training_objects.filter(Q(target='1') & Q(energy_system='1')).count())
    #print("predefined_weekly_training_objects",pred) """


    context = {
        "twohands_halfgrimp": twohands_halfgrimp,
        "twohands_openhand":  twohands_openhand,
        "onehand_halfgrimp":onehand_halfgrimp,
        "onehand_openhand": onehand_openhand,

        "long_duration_open": long_duration_open,
        "long_duration_half": long_duration_half,
        "short_duration_open": short_duration_open,
        "short_duration_half": short_duration_half,

        "pullup_endurance": pullup_endurance,
        "pullup_max": pullup_max,
    }
    print(context)
    return render(request, "analyse/analyse.html",context)
    #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')


class ChartDataHMAX(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        user = request.user
        print(user)
        dmax_model_data = Deadhang_max.objects.filter(user=request.user).order_by('date')
        serializer = DeadhangMaxSerializer(dmax_model_data, many=True)
        #return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

class ChartDataHEND(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        user = request.user
        print(user)
        dend_model_data = Deadhang_endurance.objects.filter(user=request.user).order_by('date')
        serializer = DeadhangEndSerializer(dend_model_data, many=True)
        #return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)


class ChartDataPMAX(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        user = request.user
        print(user)
        dend_model_data = Pullup_max.objects.filter(user=request.user).order_by('date')
        serializer = PullupMaxSerializer(dend_model_data, many=True)
        #return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

class ChartDataPEND(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        user = request.user
        print(user)
        dend_model_data = Pullup_endurance.objects.filter(user=request.user).order_by('date')
        serializer = PullupEndSerializer(dend_model_data, many=True)
        #return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

class ChartDataHistory(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        training_history = TrainingHistory(15, request.user)
        training_dict = training_history.get_trainingHistory()
        print(training_dict)
        return Response(json.dumps(training_dict))



class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


