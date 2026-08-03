from django.shortcuts import render, redirect, get_object_or_404
from myapp.forms import StudentForm ,CourseForm
from myapp.models import Student,Course
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CourseForm()
    return render(request, "course_create.html", {'form': form})

def home(request):
    return render(request, "home.html")

def create(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()
    return render(request, "create.html", {'form': form})


def read(request):
    students = Student.objects.all()
    return render(request, "read.html", {'students': students})


def update(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("read")
    else:
        form = StudentForm(instance=student)

    return render(request, "update.html", {"form": form})


def delete(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        return redirect("read")

    return render(request, "delete.html", {"student": student})

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('home')
    else:
        form = UserForm()
    return render(request, "signup.html", {'form': form})

def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('home')
    else:
        form = UserForm()
    return render(request, "signup.html", {'form': form})

    