from django.shortcuts import render
from django.views.generic import View
# Rest rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.request import Request

from trainingdata.models import  Deadhang_max, Deadhang_endurance, Pullup_max, Pullup_endurance
from .serializers import DeadhangMaxSerializer, DeadhangEndSerializer, PullupMaxSerializer, PullupEndSerializer
from .serializers import UserSerializer
from users.models import CustomUser
from rest_framework import generics

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


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
