from django import forms
from myapp.models import Student,Course
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'profile_pic']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'course_name']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
