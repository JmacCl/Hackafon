from django.shortcuts import render, redirect
from goals.forms import UserForm, UserProfileForm
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    context_dict = {'boldmessage':'EXAMPLE'}
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
                print('invalid')
                return HttpResponse("Invalid login details supplied.")
            
    else:
        return render(request, 'goals/login.html')