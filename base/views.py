from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from base.forms import ImageForm
from .mingo import *
from PIL import Image
from translate import translate
from django.contrib.auth.decorators import login_required
import random
from django.core.files.storage import FileSystemStorage
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash
# from .models import RegistrationForm
# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    return render(request,'base/login.html')

@login_required(login_url='login')
def homePage(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_id = request.user.id
    return render(request,'base/index.html',{'user_profile' : user_profile,'user_id': user_id})

def registerPage(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email Taken")
                return redirect('register')
            else:
                user =User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print("user created")
                return redirect('/')
        else:
            messages.info(request,"Password not matching")
            return redirect('register')
        return redirect('/')  # Redirect to the home page after registration

    else:
        return render(request,'base/register.html')

@login_required
def custom_change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        user = request.user

        # Check if the old password is correct
        if not user.check_password(old_password):
            messages.error(request, 'Incorrect old password')
            return redirect('change_password')

        # Check if the new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match')
            return redirect('change_password')

        # Set the new password and update the session auth hash
        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully')
        return redirect('home')

    return render(request, 'base/change_password.html')

def scan(request):
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            
            return render(request,'base/scan.html',{'form':form,'img_obj':img_obj})
    else:
        form = ImageForm()
        return render(request,'base/scan.html', {'form': form})
    
def result(request):
    print(request.POST)
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
                form.save()
                img_obj = form.instance
                value = prediction(img_obj.image)  
        return render(request,'base/result.html',{'form':form,'img_obj':img_obj,'value':value})
    
def update_user(request): 
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        user_profile.age = request.POST.get('age')
        user_profile.dob = request.POST.get('dob')
        user_profile.mobile = request.POST.get('mobile')
        user_profile.weight = request.POST.get('weight')
        user_profile.height = request.POST.get('height')
        user_profile.abdomen = request.POST.get('abdomen')
        user_profile.diabetic = request.POST.get('diabetic', 'not_sure')
        user_profile.profile_picture = request.FILES.get('profile_picture')

        #BMI
        weight_kg = float(user_profile.weight)
        height_m = float(user_profile.height) / 100  # Convert height to meters
        user_profile.bmi = round(weight_kg / (height_m ** 2), 2)
        
        user_profile.save()
        
        return redirect('profile')
    return render(request,'base/profile.html',{'user_profile': user_profile})

def lgout(request):
    auth.logout(request)
    return redirect('login')

def chat(request):
    L = []
    if request.method == 'POST':
        prompt_value = request.POST.get('prompt', '')
        ans = translate(prompt_value)
        L.append({'prompt': prompt_value, 'translation': ans})
        return render(request, 'base/chatbot.html', {'data': L})
    else:
        return render(request, 'base/chatbot.html')