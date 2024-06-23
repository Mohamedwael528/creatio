from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})    
   
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['PasswordConfirm']

        # التحقق من تطابق كلمات المرور
        if password != password_confirm:
            messages.error(request, 'passwords donot match')
            return redirect('register')

        # التحقق من عدم وجود اسم مستخدم مكرر
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Email is alredy exist')
            return redirect('register')

        # إنشاء مستخدم جديد
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'تم تسجيل المستخدم بنجاح. يمكنك الآن تسجيل الدخول.')
        return redirect('login')

    return render(request, 'your_app/login.html')
        
def sign_in(request):

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,'Hi {username.title()}, welcome back!')
                return redirect('/')
        
        # form is not valid or user is not authenticated
        messages.error(request,'Invalid Email or password')
        return render(request,'users/login.html',{'form': form})
    
def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('/')






         
