from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Create your models here.
#related names returns whole class
class chatrooms(models.Model):
    admin=models.ForeignKey(User, related_name="admin_of", on_delete=models.CASCADE)
    private=models.BooleanField(default=False)
    private_key=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=50,unique=True)
    total_members=models.IntegerField(default=1)
    created_on=models.DateTimeField(auto_now=True)
    members=models.ManyToManyField(User, related_name='chatroom')
    def __str__(self):
        return self.name
    def add_memeber(self,User):
        self.members.add(User)
    def remove_memeber(self,User):
        self.members.remove(User)
    def get_active_members(self):
        """Get the list of active members in the chatroom."""
        return self.members.filter(is_active=True)
    def set_private_key(self,passkey):
        self.private_key = make_password(passkey)
    def save(self,*args,**kwargs,):
        if self.private and self.private_key:
            self.set_private_key(self.private_key)
            super().save(*args,*kwargs)
        elif self.private and not self.private_key:
            raise ValueError('no passkey provided for private room')
        elif not self.private:
            super().save(*args,*kwargs)
        else:
            raise ValueError('something whent wrong')

    

       
class messages(models.Model):
    text=models.TextField()
    author=models.ForeignKey(User, related_name="my_messages", on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True)
    chatroom=models.ForeignKey(chatrooms,on_delete=models.CASCADE,related_name='messages')
    def save(self,*args, **kwargs):
        if not self.chatroom.members.filter(pk=self.author.pk).exists():
            raise ValueError('user is not a member of chatroom')
        super().save(*args,*kwargs)
    def __str__(self) -> str:
        return f"message by {self.author} in {self.chatroom.name}"