from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm
from basic_app.models import UserProfileInfo
# for login
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse('you are loged in , Nice!!')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic_app:index'))

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # this will hash the password 
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
                
            profile.save() 

            registered = True
            
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
        {'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered})

def your_profile(request):
    user_list = UserProfileInfo.objects.order_by('user')
    user_dict = {'user': user_list}
    return render(request,'basic_app/your_prof.html',context=user_dict)

def user_login(request):
    
    if request.method == "POST":   
        username = request.POST.get('username')# it will get username from (name= 'username' )html form we created in login file
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user) # this is user is return by authenticate
                return HttpResponseRedirect(reverse('basic_app:index')) # if user is login succesfully and active than he will be redirect to index page

            else:
                return HttpResponse("Accout not active")
        else:
            print("some tried to login and failed!")
            print("Username : {} and password {} ".format(username,password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request, 'basic_app/login.html',{})

