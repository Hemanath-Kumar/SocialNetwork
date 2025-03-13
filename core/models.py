from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user=get_user_model() # Fetch all user model

class profile(models.Model):

    Gender_choices=[("Male","Male"),
                    ("Female","Female")]
    
    User=models.OneToOneField(user, on_delete=models.CASCADE)
    Fullname=models.CharField(max_length=100)
    ProfileImage=models.ImageField(upload_to='profileimage',default='default\DP.png')
    Bio=models.TextField(max_length=250,blank=True)
    Gender=models.CharField(max_length=10,choices=Gender_choices,blank=True)
    UsernameTime=models.DateField(blank=True,null=True)
 
    
    def __str__(self):
        return self.Fullname

    class Meta:

        verbose_name_plural='Profile'


class post(models.Model):
    User=models.ForeignKey(user, on_delete=models.CASCADE)
    Caption=models.CharField(max_length=100,null=False)
    PostedDate=models.DateField(blank=True,null=True)
    PostedTime=models.TimeField(blank=True,null=True)
    def __str__(self):
            return f" Username: {self.User.username} [ User ID:{self.User.id}] -- [ Post ID:{self.id} ]"
     

    class Meta:

        verbose_name_plural='Post'

class postmedia(models.Model):
    PostID=models.ForeignKey(post, on_delete=models.CASCADE)
    Postimage=models.ImageField(upload_to='post')
    Imageorder=models.IntegerField(blank=True,null=True)
    
    def __str__(self):
            return  f" [ User ID:{self.PostID.User.id} ] -- [ Post ID:{self.PostID.id} ] -- [ Order : {self.Imageorder} ] "

    


    class Meta:

        verbose_name_plural='Postmedia'

class comment(models.Model):
    PostID=models.ForeignKey(post, on_delete=models.CASCADE)
    CommentUser=models.ForeignKey(user, on_delete=models.CASCADE)
    CommentMessage=models.CharField(max_length=250,blank=True)
    PostedDate=models.DateField(blank=True,null=True)
    PostedTime=models.TimeField(blank=True,null=True)
    def __str__(self):
            return  f" [ User ID:{self.CommentUser.id} ] -- [ Post ID:{self.PostID.id} ] "

    


    class Meta:

        verbose_name_plural='Comment'

class follow(models.Model):
    User=models.ForeignKey(user, on_delete=models.CASCADE,related_name="following")
    Following=models.ForeignKey(user, on_delete=models.CASCADE, related_name="followers")
    PostedDate=models.DateField(blank=True,null=True)
    PostedTime=models.TimeField(blank=True,null=True)
    def __str__(self):
            return  f" [ User:{self.User.username} ] -- [ Following:{self.Following.username} ] "


    class Meta:

        verbose_name_plural='Followercount'

class like(models.Model):
    PostID=models.ForeignKey(post, on_delete=models.CASCADE)
    Userlike=models.ForeignKey(user, on_delete=models.CASCADE)
    def __str__(self):
           return  f" [ User:{self.Userlike.username} ]"

    class Meta:

        verbose_name_plural='Like'



class saved(models.Model):
    PostID=models.ForeignKey(post, on_delete=models.CASCADE)
    UserSaved=models.ForeignKey(user, on_delete=models.CASCADE)
    def __str__(self):
           return  f" [ User:{self.UserSaved.username} ]"

    class Meta:

        verbose_name_plural='Saved'