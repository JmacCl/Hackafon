from django.shortcuts import render, redirect
from goals.forms import UserForm, UserProfileForm, GoalForm
from goals.models import UserProfile, UserGoal
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import random
from .inspirationalQuotes import quotes

from django.http import JsonResponse


def index(request):
    random_quote = random.choice(quotes)
    context_dict = {'quote_dict': random_quote, }
    if request.method == 'POST':
        post = request.POST.dict()
        for key in post.keys():
            if key.startswith("checkbox:"):
                pk_name = key.replace("checkbox:", "")
                goal = UserGoal.objects.get(pk=pk_name)
                goal.completed = True
                goal.save()

    try:
        context_dict['profile'] = UserProfile.objects.get(user=request.user)
        context_dict['goals'] = UserGoal.objects.filter(user=request.user).order_by('date')
    except:
        context_dict['profile'] = None

    return render(request, 'goals/index.html', context=context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            plain_text_password = user.password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            if not attempt_login(request, user.username, plain_text_password):
                print("failed to login")
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'goals/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if attempt_login(request, username, password):
            return redirect(reverse('goals:index'))
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'goals/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('goals:index'))


def add_goal(request):
    added = False
    if request.method == 'POST':
        add_goal_form = GoalForm(request.POST)
        if add_goal_form.is_valid():
            goal = add_goal_form.save(commit=False)
            goal.user = request.user
            goal.save()
            added = True
           
            #return redirect(reverse('goals:add_goal'))
        else:
            return HttpResponse("Missing Information")
    add_goal_form = GoalForm()

    return render(request, 'goals/add_goal.html', context={'add_goal_form': add_goal_form, 'added': added})


def attempt_login(request, username, password):
    user_auth = authenticate(username=username, password=password)
    if user_auth and user_auth.is_active:
        login(request, user_auth)
        return True

    return False

def statistics(request):
    return HttpResponse("Stats page is under development")

#Ignore, this is graph testing
def get_data(request, *args, **kwargs):
    data={
        "sales":100,
        "customers":10,
    }
    return JsonResponse(data) #http response