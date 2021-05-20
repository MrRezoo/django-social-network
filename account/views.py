from random import randint

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from account.forms import UserLoginForm, UserRegistrationForm, EditProfileForm, PhoneLoginForm, VerifyCodeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from kavenegar import *

from account.models import Profile, Relation
from posts.models import Post


def user_login(request):
    next = request.GET.get('next')
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if next:
                    redirect(next)
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


@login_required()
def user_logout(request):
    logout(request)
    messages.success(request, 'you logout successfully', 'success')
    return redirect('posts:all_posts')


@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(user=user)
    self_dash = False
    is_following = False
    relation = Relation.objects.filter(from_user=request.user, to_user=user)
    if relation.exists():
        is_following = True
    if request.user.id == user_id:
        self_dash = True
    return render(request, 'account/dashboard.html',
                  {'user': user, 'posts': posts, 'self_dash': self_dash, 'is_following': is_following})


@login_required
def profile_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user.profile,
                               initial={'email': request.user.email, 'username': request.user.username,
                                        'first_name': request.user.first_name, 'last_name': request.user.last_name})
        if form.is_valid():
            form.save()
            user.username = form.cleaned_data['username']
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'your profile edited successfully', 'success')
            return redirect('account:dashboard', user_id)

    else:
        form = EditProfileForm(instance=user.profile, initial={'email': request.user.email,
                                                               'username': request.user.username,
                                                               'first_name': request.user.first_name,
                                                               'last_name': request.user.last_name})
    return render(request, 'account/edit_profile.html', {'form': form})


def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone = f"0{form.cleaned_data.get('phone')}"
            rand_num = randint(1000, 9999)
            api = KavenegarAPI(
                '336F647455347962732F6D4D3479496B6A3642483473546C6C744D6D31774B77433473746C372B534F79453D')
            params = {
                'sender': '',
                'receptor': phone,
                'message': rand_num
            }
            api.sms_send(params)

            request.session['rand_num'] = rand_num
            request.session['phone'] = phone
            return redirect('account:verify')
    else:
        form = PhoneLoginForm()
    return render(request, 'account/phone_login.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            rand_num = request.session['rand_num']
            phone = request.session['phone']
            if rand_num == form.cleaned_data.get('code'):
                profile = get_object_or_404(Profile, phone=phone)
                user = get_object_or_404(User, profile__id=profile.id)
                login(request, user)
                messages.success(request, 'logged in successfully', 'success')
                return redirect('posts:all_posts')
            else:
                raise messages.error(request, 'your code is wrong', 'danger')
    else:
        form = VerifyCodeForm()
    return render(request, 'account/verify.html', {'form': form})


@login_required
def follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status': 'exists'})
        else:
            Relation(from_user=request.user, to_user=following).save()
            return JsonResponse({'status': 'ok'})


@login_required
def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not_exists'})
