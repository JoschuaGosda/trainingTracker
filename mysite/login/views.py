from django.shortcuts import render, redirect
from .forms import  SignInForm, SignUpForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from users.models import CustomUser as User
from django.core.mail import EmailMessage

from trainingdata import urls

# def create_person(request):
# 	if request.method == "POST":
# 		form = PersonForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			form = PersonForm()
	# else:
	# 	form = PersonForm()
	# return render(request, "person/create_person.html", {'form': form})

def login(request):
	if request.method == "POST":
		form = SignInForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)

			print(user)
			if user is not None:
				auth_login(request, user)
				#return HttpResponseRedirect('/')
				return redirect('record_list')
			else:
				return HttpResponseRedirect('/please-check-your-email/')
	else:
		form = SignInForm()
	return render(request, "registration/login.html",{'form': form})

def index(request):
	if request.user.is_authenticated:
		return redirect('record_list')
	else:
		return render(request, "base/index.html",{})

		
    #return render(request, "person/create_person.html", {})

# def signup(request):
# 	User = get_user_model()
# 	if request.method == 'POST':
# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data.get('username')
# 			raw_password = form.cleaned_data.get('password1')
# 			user = authenticate(username=username, password=raw_password)
# 			auth_login(request, user)
# 			return redirect('/')
# 	else:
# 		form = SignUpForm()
# 	return render(request, 'registration/signup.html', {'form': form})
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your account.'
			message = render_to_string('emails/acc_activate_email.html',{
			'user':user,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
			mail_subject, message, to=[to_email]
			)
			email.send()
			return render(request, 'registration/pleaseconfirm.html',{})
	else:
		form = SignUpForm()
	return render(request, 'registration/signup.html',{'form':form})





# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your blog account.'
#             message = render_to_string('emails/acc_activate_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
# 			return render(request, 'registration/pleaseconfirm.html',{})
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #auth_login(request, user)
        return redirect('login')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
