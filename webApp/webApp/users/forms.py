from django import forms
from django.contrib.auth.forms import UserCreationForm
from webApp.users.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email_address', 'phone', 'country', 'city', 'address', 'company', 'school', 'image')
