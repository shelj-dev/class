from django import forms
from django.contrib.auth.models import User
from .models import Todo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name','email']


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']
