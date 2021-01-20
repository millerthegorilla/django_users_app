# users/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_username(self):
      username = self.cleaned_data['username']
      if User.objects.filter(email=username):
        self.add_error('username', 'Error, That username already exists!')
      return username

    def clean_email(self):
      email = self.cleaned_data['email']
      if User.objects.filter(email=email):
        self.add_error('email', 'Error! That email already exists!')
      return email


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['personal_statement']

