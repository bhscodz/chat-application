from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
#related names returns whole class
class chatrooms(models.Model):
    admin=models.ForeignKey(User, blank=False, related_name="admin_of", on_delete=models.CASCADE,editable=False)
    private_key=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=50,unique=True)
    total_members=models.IntegerField(
        default=1,
        validators=[MaxValueValidator(100),MinValueValidator(2)]
    )
    current_member=models.IntegerField(default=0,blank=False,editable=False)
    created_on=models.DateTimeField(auto_now=True)
    members=models.ManyToManyField(User, related_name='member_of',blank=True,editable=False)
    banned_member=models.ManyToManyField(User,blank=True,editable=False,related_name='banned_from')
    
    def __str__(self):
        return self.name
    
    def add_member(self,User):
        if self.total_members>self.current_member:
            self.members.add(User)
            self.current_member=self.current_member+1
            self.save()
        else:
            raise ValueError('room is full')
    
    def remove_member(self,User):
        self.members.remove(User)
        self.current_member=self.current_member-1
        self.save()
    
    def ban_member(self,User):
        self.banned_member.add(User)
        self.remove_member(User)
    

    def get_active_members(self):
        """Get the list of active members in the chatroom."""
        return self.members.filter(is_active=True)
    

    

       
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