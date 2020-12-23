from django import forms
from users.models import CustomUser as User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm

# class PersonForm(forms.ModelForm):
# 	class Meta:
# 		model = Person
# 		fields = '__all__'

class SignInForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput())


	def clean_username(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		try:
			self.user = User.objects.get(username=self.cleaned_data['username'])
		except User.DoesNotExist:
			self.user = None
			raise forms.ValidationError("No matching registered user")
		return username


	def clean_password(self, *args, **kwargs):
		password = self.cleaned_data.get('password', None)
		if not self.user==None:
			sucess = self.user.check_password(password)
			if not sucess:
				raise forms.ValidationError('Invalid password')
		return password

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
