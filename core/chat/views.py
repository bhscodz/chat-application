from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .decorators import *
from django.contrib.auth.hashers import make_password
from . import models
# Create your views here.
#Managers are accessible only via model classes, rather than 
# from model instances, to enforce a separation 
# between “table-level” operations and “record-level” operations.
# vimpnote use filter to get a query set and get get a single result
# django template engine does not compare model instances in same way as
#python does it can only compare strings and it cant also index lists
# python compare model instances by comparing all fields including pk value
#also we can tell it what to caompare but if you simply equate objects it does so
from .forms import CreateUserForm,room_creationform
def index(request):
    form=room_creationform()
    if request.user.is_authenticated:
        room_admin=User.objects.get(username=request.user.username).admin_of.all()
        room_member=request.user.member_of.all().exclude(admin=request.user)
        print(room_member)
        messages.info(request,f'welcome {request.user.username}')
        return render(request,'index.html',{'form':form,'myroom':room_admin,'room_member':room_member})
    else:
        messages.info(request,f'you are {request.user} plz login')
    return render(request,'index.html',{'form':form})

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


""" chat room creation api """
@login_required
def create_room(request):
    user_obj=models.User.objects.get(username=request.user)
    if request.method=='POST':
        form=room_creationform(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            if room.private_key:
                room.private_key=make_password(room.private_key)
            else:
                pass
            room.admin=user_obj
            room.save()
            room_obj=models.chatrooms.objects.get(name=request.POST.get('name'))
            room.add_member(user_obj)
            data={'admin':room.admin.username,'roomname':room.name,
                  'isadmin':room.admin.username==request.user}
            response=JsonResponse(data,status=200)
            return response
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            response=JsonResponse(form.errors,status=400)
            return response
    else:
        return JsonResponse({'data':'bad_request'},status=400)
   
""" chat room """
@login_required
@banned_from_entering
@process_membership
def room(request ,room_name):
    obj = get_object_or_404(models.chatrooms, name=room_name) 
    all_messages=obj.messages.all()
    messages.info(request,f'welcome to chat room {request.user.username}')
    return render(request,'chatroom.html',{'room_name':room_name,'room_obj':obj,'members':obj.members.all(),'all_messages':all_messages})

""" banned losers """
def banned(request):
    return render(request,'banned.html')

@login_required
@banned_from_entering
def add_member_to_room(request,room_name):
    room_obj=models.chatrooms.objects.get(name=room_name)
    user_obj=models.User.objects.get(username=request.user.username)
    if request.user in room_obj.members.all():
        return redirect(f'/chat/{room_name}')
    elif not room_obj.private_key:
        return redirect(f'/chat/{room_name}')
    else:
        if request.method=='POST':
            key=request.POST.get('key')
            print(make_password(key),room_obj.private_key)
            if check_password(str(key),room_obj.private_key):
                room_obj.add_member(user_obj)
                return redirect(f'/chat/{room_name}')
            else:
                return render(request,'add_member.html',{'room_name':room_name,'error':'private key mismatch'})
    return render(request,'add_member.html',{'room_name':room_name})

@login_required
def ban_member_request(request):
    if request.method=='POST':
        room_name=request.POST.get('room_name')
        username=request.POST.get('username')
        candidate=get_object_or_404(models.User,username=username)
        if is_admin(request.user,room_name) and candidate!= request.user:
            room_obj=get_object_or_404(models.chatrooms,name=room_name)
            if candidate in room_obj.members.all():
                print(room_obj.members.all())
                room_obj.ban_member(candidate)
                return JsonResponse({'data':f'succesfuly removed {candidate}'})
            else:
                return JsonResponse({'data':'member not present in room'},status=404)
        else:
            return JsonResponse({'data':'not authorised'},status=401)
    else:
        return JsonResponse({'data:bad request'},status=400)

@login_required
def move_out(request):
    if request.method=='POST':
        room_name=request.POST.get('roomname')
        try:
            room_obj=get_object_or_404(models.chatrooms,name=room_name)
        except:
            return JsonResponse({'data':'room dosent exist or might be delted refresh the page and try again'},status=400)
        if is_member(request.user,room_name):
            print('is_member',room_obj.members.all())
            if is_admin(request.user,room_name):
                return JsonResponse({'data':'admin can only delete room not move out'},status=404)
            else:
                room_obj.remove_member(request.user)
                return JsonResponse({'data':f'done user {request.user} removed from {room_name}'},status=200)
        else:
            return JsonResponse({'data':'you are not the member you might be removed by admin plz relod the page'},status=404)
    else:
        return JsonResponse({'data':'error'},status=403)

@login_required
def delete_room(request):
    if request.method=='POST':
        room_name=request.POST.get('roomname')
        if is_admin(request.user,room_name):
            models.chatrooms.objects.get(name=room_name).delete()
            return JsonResponse({'data':'room deleted sucessfully'},status=200)
        else:
            return JsonResponse({'data':'not authorized'},status=401)
    else:
        return JsonResponse({'data':'404 not allowed'})
    
def all_data(request):
    list1=[]
    room_obj=models.chatrooms.objects.all()
    for obj in room_obj:
        l=[]
        l.append(obj.name)
        l.append(obj.admin)
        l.append(obj.private_key)
        l.append(obj.total_members)
        l.append(obj.current_member)
        l.append(obj.current_member)
        l.append(obj.members.all())
        l.append(obj.banned_member.all())
        list1.append(l)
    return render(request,'data.html',{'rooms':list1})