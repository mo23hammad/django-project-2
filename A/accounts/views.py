from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm,UserRegisterVerifyForm,UserLoginForm
from .models import OtpCode,User
import random
from datetime import timedelta,datetime
from .tasks import send_otp_code_task

class UserRegisterView(View):
    form_class = UserRegisterForm

    def get(self,request):
        form = self.form_class()
        return render(request, 'accounts/register.html',{'form':form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000,9999)
            send_otp_code_task(form.cleaned_data['phone_number'],random_code)
            OtpCode.objects.create(phone_number = form.cleaned_data['phone_number'],code = random_code)
            request.session['user_registration_info'] = {
                'email':form.cleaned_data['email'],
                'phone_number':form.cleaned_data['phone_number'],
                'full_name':form.cleaned_data['full_name'],
                'password':form.cleaned_data['password']
            }
            messages.success(request,'A code just sent to your phone number','success')
            return redirect('accounts:verify_code')
        return render(request,'accounts/register.html',{'form':form})
   

class UserRegisterVerifyCodeView(View):
    form_class = UserRegisterVerifyForm

    def get(self,request):
        form = self.form_class()
        return render(request,'accounts/verify.html',{'form':form})
    def post(self,request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():

            cd = form.cleaned_data
            now = datetime.now
            expiry_time = now - timedelta(minutes=2)
            if cd['code'] == code_instance.code and expiry_time < now:
                User.objects.create_user(phone_number = user_session['phone_number'],email = user_session['email'],
                                         full_name = user_session['full_name'],password = user_session['password'])
                code_instance.delete()
                messages.success(request,'you registered successfully','success')
                return redirect('home:home')
            else:
                messages.error(request,'your code is not valid','danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get(next)
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class()
        return render(request,'accounts/login.html',{'form':form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,phone_number = cd['phone_number'],password = cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in successfully','success')
                return redirect('home:home')
            else:
                messages.error(request,'your phone number or password is not correct')
                return redirect('accounts:user_login')
        return redirect('home:home')


class UserLogoutView(LoginRequiredMixin,View):
    
    def get(self,request):
        logout(request)
        messages.success(request,'you logged out successfully','success')
        return redirect('home:home')
        
