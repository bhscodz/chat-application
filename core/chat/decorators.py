#VIMP when we are using multiple decorators it wraps one inside other
#first decorator takes remaining part inside and wraps it then second and so on
#the behaviour of how function unwraps completely depends on how decorators are
#written if you check things first then execute function then it just gets in other decorator
#so it just depends on how a decorator is written and implimented
#also real function executes only inside the center of this onion but the thing is that
#we need to figure out how many wrappers remail efffective after it

from . import models
from . import views
from django.shortcuts import redirect,render,HttpResponse,get_object_or_404
""" this decorator should always be used after login_required """
def process_membership(fnc):
    def wrapper(request,room_name,*args,**kwargs):
        room_obj=get_object_or_404(models.chatrooms,name=room_name)
        print('i am decorator')
        if request.user in room_obj.members.all():
            result= fnc(request,room_name)
        else:
            if room_obj.private_key:
                result=redirect(f'/chat/add_member/{room_obj.name}')
            else:
                try:
                    room_obj.add_member(request.user)
                    result=fnc(request,room_name)
                except Exception as e:
                    result=HttpResponse(f'{e} this room is full')
        return result
    return wrapper

""" this decorator should always be used after login_required """
def banned_from_entering(fun):
    def wrapper(request,room_name,*args, **kwargs):
        user=request.user
        room_obj=get_object_or_404(models.chatrooms,name=room_name)
        print('banned in check')
        if user in room_obj.banned_member.all():
            result=redirect('banned')
        else:
            result=fun(request,room_name,*args, **kwargs)
        return result
    return wrapper

def is_admin(user,room_name):
    if user==get_object_or_404(models.chatrooms,name=room_name).admin:
        return True
    else:
        return False
def is_member(user,room_name):
    room_obj=get_object_or_404(models.chatrooms,name=room_name)
    print(room_obj)
    if user in room_obj.members.all():
        return True
    else:
        return False
    