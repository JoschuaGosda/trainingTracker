from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.views import View
from trainingdata.models import Leaderboard
from trainingdata.forms import Leaderboard_Form
from users.models import CustomUser

# Create your views here.


# @login_required
# def leaderboard(request):
#
#     return render(request, "trainingdata/leaderboard_list.html",{})

class LeaderboardView(View):
    def get(self, request):
        # <view logic>
        users = CustomUser.objects.all()
        leaderboard = Leaderboard.objects.all()
        dict_time = {}
        if leaderboard.count() > 0:
            for user in users:
                    time = leaderboard.filter(user=user).aggregate(Max('time'))
                    if time['time__max'] is not None:
                        dict_time.update({user.username: time['time__max']})
            sorted_dict_time = dict(sorted(dict_time.items(), key=lambda x:x[1], reverse=True))
            print(dict(sorted_dict_time))
        else:
            sorted_dict_time = {}

        form = Leaderboard_Form()
        context = {
            "leaderboard_dict": sorted_dict_time,
            "form": form,
        }
        return render(request, "trainingdata/leaderboard_list.html",context)

    def post(self, request):
        form = Leaderboard_Form(request.POST)
        if form.is_valid():
            
            user = request.user
            #print(form.cleaned_data)
            obj, created = Leaderboard.objects.update_or_create(
                user=user,
                defaults={'time': form.cleaned_data['time']},
            )
            return redirect('leaderboard_list')
        else:
            return redirect('index_site')
            #form = Deadhang_max_Form()
