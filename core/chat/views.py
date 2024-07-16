from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import CreateUserForm,room_creationform
def index(request):
    form=room_creationform()
    if request.user.is_authenticated:
        messages.info(request,f'welcome {request.user.username}')
    else:
        messages.info(request,f'you are {request.user} plz login')
    return render(request,'index.html',{'form':form})

@login_required
def room(request ,room_name):
    messages.info(request,f'welcome to chat room {request.user.username}')
    return render(request,'chatroom.html',{'room_name':room_name})

def signin(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile details updated.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
                    messages.error(request,f"Field: {field}, Error: {error}")
     
    else:
        messages.info(request, "hello new user")
    return render(request,'signup.html',{'page_name':'signin','form':form})
def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password is incorrect')
    messages.info(request,'login is required!')
    return render(request,'login.html')
def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def create_room(request):
    if request.method=='POST':
        form=room_creationform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "room succesfully created")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
                    messages.error(request,f"Field: {field}, Error: {error}")
    else:
        return redirect('home')
    return redirect('home')
