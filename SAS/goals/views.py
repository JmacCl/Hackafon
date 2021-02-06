from django.shortcuts import render, redirect
from goals.forms import UserForm, UserProfileForm, GoalForm
from goals.models import UserProfile
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    context_dict = {}

    try:
        context_dict['profile']=UserProfile.objects.get(user=request.user)
    except:
        context_dict['profile']="ono"

    return render(request, 'goals/index.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user


            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'goals/register.html', context = {'user_form':user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('goals:index'))
            else:
                return HttpResponse("Invalid login details supplied.")
        else:
             print('invalid')
             return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'goals/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('goals:index'))
    
def addGoal(request):
    if request.method == 'POST':
        addGoal_form = GoalForm(request.POST)
        if addGoal_form.is_valid():
            goal = addGoal_form.save(commit=False)
            goal.user = request.user
            goal.save()
        else:
            return HttpResponse("Missing Information")
    else:
        addGoal_form = GoalForm()
        
    return render(request, 'goals/addGoal.html', context = {'addGoal_form': addGoal_form})