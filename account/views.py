from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from account.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('posts:all_posts')
            else:
                messages.success(request, 'wrong username or password', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            messages.success(request, 'you registered successfully', 'success')
            login(request, user)
            return redirect('posts:all_posts')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'you logout successfully', 'success')
    return redirect('posts:all_posts')


def user_dashboard(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'account/dashboard.html', {'user': user})
