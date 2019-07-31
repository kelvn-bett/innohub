from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comments

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]
CAT_CHOICES = [
    ('I', 'IT'),
    ('H', 'Human Resource'),
    ('F', 'Finance'),
    ('HE', 'Health'),
    ('B', 'Business'),
    ('A', 'Agriculture'),
    ('E', 'Entertainment'),
]


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    category = forms.ChoiceField(choices=CAT_CHOICES)
    phone_number = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'category', 'phone_number', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body', ]
