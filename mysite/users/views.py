from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.views import View
from users.models import CustomUser
from trainingdata.models import Deadhang_max

# Create your views here.


# @login_required
# def leaderboard(request):
#
#     return render(request, "trainingdata/leaderboard_list.html",{})

class LeaderboardView(View):
    def get(self, request):
        # <view logic>
        users = CustomUser.objects.all()
        dmax_objects = Deadhang_max.objects.all()
        dict_maxStrength = {}
        if dmax_objects.count() > 0:
            for user in users:
                    relative_strength = dmax_objects.filter(user=user).aggregate(Max('relative_strength'))
                    if relative_strength['relative_strength__max'] is not None:
                        dict_maxStrength.update({user.username: relative_strength['relative_strength__max']})
            sorted_dict_maxStrength = dict(sorted(dict_maxStrength.items(), key=lambda x:x[1], reverse=True))
            print(dict(sorted_dict_maxStrength))
        else:
            sorted_dict_maxStrength = {}

        context = {
            "leaderboard_dict": sorted_dict_maxStrength,
        }
        return render(request, "trainingdata/leaderboard_list.html",context)

