from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm, TodoForm
from .models import Todo

# SIGNUP
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = UserForm()
    return render(request, "signup.html", {"form": form})

# LOGIN
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # ✅ login user properly
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# LOGOUT
def logout_view(request):
    logout(request)  # destroys session
    return redirect("login")

# TODO/HOME (PROTECTED)
@login_required(login_url='login')  # ✅ only logged-in users can access
def home(request):
    todos = Todo.objects.filter(user=request.user)

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect("home")
    else:
        form = TodoForm()

    return render(request, "home.html", {"form": form, "todos": todos})

# DELETE TODO (optional, also login required)
@login_required(login_url='login')
def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()
    return redirect("home")
