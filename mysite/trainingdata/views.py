from django.shortcuts import render, redirect
from .forms import Deadhang_max_Form, Deadhang_endurance_Form, Pullup_max_Form, Pullup_endurance_Form, CustomSession_Form
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Deadhang_max, Deadhang_endurance, Pullup_max, Pullup_endurance, Training, CustomSession
from users.models import CustomUser
from django.db.models import Q

from django.utils import timezone
from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.detail import DetailView




# def index(request):
#     #return HttpResponse("Hello, world. You're at the trainingdata index.")
#     return render(request, "trainingdata/create_training.html",{}) #no need to set /templastes before

@login_required
def create_deadhang_max(request):
    if request.method == "POST":
        form = Deadhang_max_Form(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            user = request.user
            date = datetime.date(fs.date)
            fs.user = user
            Training.objects.create(title='d1', user=user, date=date)
            fs.training = Training.objects.filter(user=user).last()
            fs.session_counter = Deadhang_max.objects.filter(user=user).count()+1
            fs.save()
            return redirect('record_list')
            #form = Deadhang_max_Form()
    else:
        form = Deadhang_max_Form()
    return render(request, "trainingdata/create_deadmax.html", {'form': form})


@login_required
def create_deadhang_endurance(request):
    if request.method == "POST":
        form = Deadhang_endurance_Form(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            user = request.user
            date = datetime.date(fs.date)
            fs.user = user
            Training.objects.create(title='d2', user=user, date=date)
            fs.training = Training.objects.filter(user=user).last()
            fs.session_counter = Deadhang_endurance.objects.filter(user=user).count()+1
            fs.save()
            return redirect('record_list')
            #form = Deadhang_endurance_Form()
    else:
        form = Deadhang_endurance_Form()
    return render(request, "trainingdata/create_deadendurance.html", {'form': form})

@login_required
def create_pullup_endurance(request):
    if request.method == "POST":
        form = Pullup_endurance_Form(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            user = request.user
            date = datetime.date(fs.date)
            fs.user = user
            Training.objects.create(title='p2', user=user, date=date)
            fs.training = Training.objects.filter(user=user).last()
            fs.session_counter = Pullup_endurance.objects.filter(user=user).count()+1
            fs.save()
            return redirect('record_list')
            #form = Pullup_endurance_Form()
    else:
        form = Pullup_endurance_Form()
    return render(request, "trainingdata/create_pullupendurance.html", {'form': form})

@login_required
def create_pullup_max(request):
    if request.method == "POST":
        form = Pullup_max_Form(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            user = request.user
            date = datetime.date(fs.date)
            fs.user = user
            Training.objects.create(title='p1', user=user, date=date)
            fs.training = Training.objects.filter(user=user).last()
            fs.session_counter = Pullup_max.objects.filter(user=user).count()+1
            fs.save()
            return redirect('record_list')
            #mylastquery = Pullup_max.objects.filter(user=request.user).last()
            #mylastquery.objects.update(weight=400)
            #print(Pullup_max.objects.filter(user=request.user).last().training)
            #Pullup_max.objects.filter(user=request.user).update(weight=200)
            #print(Pullup_max.objects.filter(user=request.user).last().weight)
            # latest_pmax_obj = Pullup_max.objects.filter(user=request.user).last()
            # latest_pmax_obj.weight = 14
            # print(latest_pmax_obj.weight)
            # latest_pmax_obj.training = Training.objects.filter(user=request.user).last()
            #form = Pullup_max_Form()
    else:
        form = Pullup_max_Form()
    return render(request, "trainingdata/create_pullupmax.html", {'form': form})


@login_required
def create_custom_training(request):
    if request.method == "POST":
        form = CustomSession_Form(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            user = request.user
            date = datetime.date(fs.date)
            fs.user = user
            Training.objects.create(title='c', user=user, date=date)
            fs.training = Training.objects.filter(user=user).last()
            # fs.session_counter = Pullup_endurance.objects.filter(user=user).count()+1
            fs.save()
            return redirect('record_list')
            #form = Pullup_endurance_Form()
    else:
        form = CustomSession_Form()
    return render(request, "trainingdata/create_custom.html", {'form': form})


class RecordListView(ListView ):
    template_name = "trainingdata/training_list.html"
    model = Training
    #paginate_by = 5  # if pagination is desired


    def get_queryset(self, *args, **kwargs):
        queryset = Training.objects.filter(user=self.request.user).order_by('date').reverse()
        return queryset

class RecordListView_Max(ListView ):
    template_name = "trainingdata/training_list.html"
    model = Training
    #paginate_by = 5  # if pagination is desired


    def get_queryset(self, *args, **kwargs):
        queryset = Training.objects.filter(user=self.request.user).filter(Q(title='d1') | Q(title='p1')).order_by('date').reverse()
        return queryset

class RecordListView_End(ListView ):
    template_name = "trainingdata/training_list.html"
    model = Training
    #paginate_by = 5  # if pagination is desired


    def get_queryset(self, *args, **kwargs):
        queryset = Training.objects.filter(user=self.request.user).filter(Q(title='d2') | Q(title='p2')).order_by('date').reverse()
        return queryset


#queryset = Training.objects.filter(user=self.request.user).exclude(title='d1').order_by('date').reverse()





# class DeadhangMaxDetailView(DetailView):
#     template_name = "trainingdata/dmax_detail.html"
#     model = Deadhang_max
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = Deadhang_max.objects.filter(user=self.request.user)
#         return queryset
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
# class DeadhangEndDetailView(DetailView):
#     template_name = "trainingdata/dend_detail.html"
#     model = Deadhang_endurance
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = Deadhang_endurance.objects.filter(user=self.request.user)
#         return queryset
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
# class PullupMaxDetailView(DetailView):
#     template_name = "trainingdata/pmax_detail.html"
#     model = Pullup_max
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = Pullup_max.objects.filter(user=self.request.user)
#         return queryset
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
# class PullupEndDetailView(DetailView):
#     template_name = "trainingdata/pmax_detail.html"
#     model = Pullup_endurance
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = Pullup_endurance.objects.filter(user=self.request.user)
#         return queryset
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

class DeadhangMaxUpdateView(UpdateView):
    template_name = "trainingdata/dmax_update_form.html"
    model = Deadhang_max
    fields = ['date','hand_position', 'hands', 'weight', 'crimp_size', 'sets','comment']
    template_name_suffix = '_update_form'
    def get_queryset(self, *args, **kwargs):
        queryset = Deadhang_max.objects.filter(user=self.request.user)
        return queryset

class DeadhangEndUpdateView(UpdateView):
    template_name = "trainingdata/dend_update_form.html"
    model = Deadhang_endurance
    fields = ['date','hand_position', 'hold_duration','weight', 'crimp_size','level', 'sets', 'repetitions','comment']
    template_name_suffix = '_update_form'
    def get_queryset(self, *args, **kwargs):
        queryset = Deadhang_endurance.objects.filter(user=self.request.user)
        return queryset

class PullupMaxUpdateView(UpdateView):
    template_name = "trainingdata/pmax_update_form.html"
    model = Pullup_max
    fields = ['date', 'weight', 'sets', 'repetitions','comment']
    template_name_suffix = '_update_form'
    def get_queryset(self, *args, **kwargs):
        queryset = Pullup_max.objects.filter(user=self.request.user)
        return queryset

class PullupEndUpdateView(UpdateView):
    template_name = "trainingdata/pend_update_form.html"
    model = Pullup_endurance
    fields = ['date', 'sets', 'repetitions','comment']
    template_name_suffix = '_update_form'
    def get_queryset(self, *args, **kwargs):
        queryset = Pullup_endurance.objects.filter(user=self.request.user)
        return queryset

# class DeadhangMaxDeleteView(DeleteView):
#     model = Deadhang_max
#     success_url = reverse_lazy('record_list')

class CustomTrainingUpdateView(UpdateView):
    template_name = "trainingdata/custom_update_form.html"
    model = CustomSession
    fields = ['title','date', 'energy_system', 'target', 'repetitions','on_off_time','sets','weight','crimp_size','comment']
    template_name_suffix = '_update_form'
    def get_queryset(self, *args, **kwargs):
        queryset = CustomSession.objects.filter(user=self.request.user)
        return queryset

class TrainingDeleteView(DeleteView):
    model = Training
    success_url = reverse_lazy('record_list')

# class DeadhangMaxDetailView(DetailView):
#
#     model = Deadhang_max
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context
