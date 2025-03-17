from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from .models import  profile,post,postmedia,comment,follow,like,saved
from django.contrib.auth.decorators import login_required
import datetime
from django.forms.models import model_to_dict
# Create your views here.


def signup_page(request):

    if request.method == "POST":
        fullname=request.POST['fullname']
        username=request.POST['username']
        emailaddress=request.POST['emailaddress']
        password=request.POST['password']
        
        
        if User.objects.filter(username=username).exists():
            pass
        
        if User.objects.filter(email=emailaddress).exists():
            pass
         
        else:
            if username and emailaddress and password:
                u=User.objects.create(username=username,email=emailaddress)
                u.set_password(password)
                u.save()
            else:
                messages.add_message(request, messages.INFO, "Fill all the details")

                return redirect('signup')

            user_login=authenticate(request,username=username,password=password)
            login(request,user_login)

            user=User.objects.get(username=username)
            profile_creation=profile.objects.create(User=user,Fullname=fullname)
            profile_creation.save()


            return redirect("setting")

    return render(request,'signup\signup.html')


def check_username(request):
    username = request.GET.get('username')

    if username:
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'})


def check_gmail(request):
    email= request.GET.get('email')
   
    if email:
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'})



def signin_page(request):

    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("home")

        else:
                messages.add_message(request, messages.INFO, "Invalid password")

                return redirect('signin')

    return render(request,'signin\signin.html')

@login_required(login_url="signin")
def setting_page(request):
   
    user_profile=profile.objects.get(User=request.user)
    
    if request.method == "POST":
        
        fullname=request.POST['fullname']
        bio=request.POST['bio']
        gender=request.POST['gender']
        
        
        if fullname:
            user_profile.Fullname=fullname
                
        if gender  in ["None","Male", "Female"]:
            user_profile.Gender=gender

        user_profile.Bio=bio
            
        user_profile.save()

        return redirect("setting")
    return render(request,"setting\setting.html",{'profile':user_profile})


# separate the form in setting page
@login_required(login_url="signin")
def profile_photo_change(request):

    user_profile=profile.objects.get(User=request.user)

    if request.method == "POST" and request.FILES.get('profileimage'):
        
        if request.FILES.get('profileimage') != None:

            profileimage=request.FILES.get('profileimage')
            user_profile.ProfileImage=profileimage
            user_profile.save()
            return redirect("setting")
    return redirect("setting")



@login_required(login_url="signin")
def home_page(request):

    user=User.objects.get(username=request.user.username)
    user_profile=profile.objects.get(User=user)

    followings=follow.objects.filter(User=user)
    
    following_post=[]
    following_post_media=[]

    for following in followings:
        
        try:

            posts=post.objects.filter(User=following.Following)
            following_post +=posts
        
        except UnboundLocalError:
            pass

    for i in following_post:
        
        following_post_media +=postmedia.objects.filter(PostID=i)

    following_post.reverse()
    return render(request,"home\home.html",{"user_profile":user_profile,
                                            "postdetails":following_post,
                                            "postmedias":following_post_media})



@login_required(login_url="signin")
def logout_page(request):
    logout(request)
    request.session.flush() 
    return redirect("signin")



@login_required(login_url="signin")
def username_edit_page(request):

    user_profile=profile.objects.get(User=request.user)

    user=User.objects.get(username=user_profile.User.username)

    if request.method == "POST":
        
        if user_profile.UsernameTime:
            
            currentdate=datetime.date.today() #Get current date

            tdelat=datetime.timedelta(days=10) #Get 10 days 

            privousdatetime=currentdate - tdelat
      
            if privousdatetime  >= user_profile.UsernameTime:

                if request.method == "POST":
                
                    username=request.POST['username']

                    if username:
                        user.username=username
                        user.save()
                        user_profile.UsernameTime=datetime.date.today()
                        user_profile.save()

                    return redirect("setting")

            else:
                pass
        else:
            if request.method == "POST":
      
                username=request.POST['username']
                if username:
                    user.username=username
                    user.save()
                    user_profile.UsernameTime=datetime.date.today()
                    user_profile.save()

    return redirect("setting")


@login_required(login_url='signin')
def post_upload(request):

    user=User.objects.get(username=request.user.username)
    currentdate=datetime.date.today()
    currenttime=datetime.datetime.now().strftime("%H:%M:%S")
    if request.method == "POST" and request.FILES.get('postimage'):
        caption=request.POST['caption']

        postimages=request.FILES.getlist('postimage')

        Creating_post=post.objects.create(User=user,Caption=caption,
                                          PostedDate=currentdate,
                                          PostedTime=currenttime)
        Creating_post.save()

        order=0
        for postimage in postimages:
            Creating_postmedia=postmedia.objects.create(PostID=Creating_post,
                                                        Postimage=postimage,Imageorder=order)
            order+=1
            Creating_postmedia.save()

        
    return redirect("/")



@login_required(login_url="signin")
def profile_page(request,username):
   
    user=User.objects.get(username=username)
    user_profile=profile.objects.get(User=user)
    
    posts=post.objects.filter(User=user)


    #***************************************************************
    # This line of code is used to follower and following count .

    followingcount=follow.objects.filter(User=user).count()
    followercount=follow.objects.filter(Following=user).count()

    #***************************************************************




    postdetail=list(posts) #It add all the post belong to this profile.
    postmediacontent=[] 


    for i in posts:

        media=postmedia.objects.filter(PostID=i) # It check list of images in specfic ID and filter it.
        postmediacontent += media#It add each image from fitered media variable.

      
    postdetail.reverse()
    return render(request,"profile\profile.html",{"user_profile":user_profile,
                                            "postdetails":postdetail,
                                            "postmedias":postmediacontent,
                                            "followingcount":followingcount,
                                            "followercount":followercount
                                            })

@login_required(login_url="signin")
def get_comment_model(request):
    
    username= request.GET.get('username')
    postid= request.GET.get('postid')
    user=User.objects.get(username=username)

    user_posts=post.objects.get(User=user,id=postid)

    postcomment=[]
   
    try:
        user_comments=comment.objects.filter(PostID=user_posts) # Ensure field name matches model
        for user_comment in user_comments:

            user=User.objects.get(username=user_comment.CommentUser.username)
            comment_profile=profile.objects.get(User=user)
            
            postcomment.append(model_to_dict(user_comment)) 


            last_insert_comment_object=postcomment[-1]
            last_insert_comment_object["CommentUser"]=user.username   
            last_insert_comment_object["CommentUserFullname"]=comment_profile.Fullname
            last_insert_comment_object["image"]=request.build_absolute_uri(comment_profile.ProfileImage.url)
        postcomment.reverse()
        
        return JsonResponse({"data": postcomment})
    
    except User.DoesNotExist:
        return HttpResponse(status=204) 
    
@login_required(login_url="signin")
def comment_send_model(request,username,postid):

    commenting_profile_post=post.objects.get(id=postid)


    commentuser=User.objects.get(username=username)
    
    if request.method == "POST":
        commentMessage=request.POST['comment']
        recive=comment.objects.create(PostID=commenting_profile_post,
                                  CommentUser=commentuser,
                                  CommentMessage=commentMessage)
        recive.save()
    
    return HttpResponse(status=204) 


@login_required(login_url="signin")
def follow_count(request):

    username= request.GET.get('username')
    user=User.objects.get(username=request.user.username)
    
    try:
        following=User.objects.get(username=username)

        check_user_already_following=follow.objects.filter(User=user,Following=following)

        #Check true are false of userfollowing to this profile.
        if check_user_already_following.exists(): 
            
            check_user_already_following.delete()
            userfollowing=False

        else:

            follow.objects.create(User=user,Following=following)
            userfollowing=True
   
    except User.DoesNotExist:
            return HttpResponse(status=204) 
    
    

    return JsonResponse({"data": userfollowing})



@login_required(login_url="signin")
def follow_status(request):

    username= request.GET.get('username')
    user=User.objects.get(username=request.user.username)
    
    try:
        following=User.objects.get(username=username)

        check_user_already_following=follow.objects.filter(User=user,Following=following)

        if check_user_already_following.exists():
            userfollowing=True   

        else:    
            userfollowing=False
   
    except User.DoesNotExist:
            return HttpResponse(status=204) 
    

    return JsonResponse({"data": userfollowing})  


@login_required(login_url="signin")
def following_page(request,username):

    
    user=User.objects.get(username=username)
    user_profile=profile.objects.get(User=user)

    following=follow.objects.filter(User=user)

    return render(request,"following/following.html",{ "user_profile":user_profile,
                                                        "followings":following
                                                        })


@login_required(login_url="signin")
def follower_page(request,username):
    user=User.objects.get(username=username)
    user_profile=profile.objects.get(User=user)

    follower=follow.objects.filter(Following=user)

    return render(request,"follower/follower.html",{ "user_profile":user_profile,
                                                        "followers":follower
                                                        })


@login_required(login_url="signin")
def user_like(request):

    postid= request.GET.get('postid')
    Postid=post.objects.get(id=postid)
    user=User.objects.get(username=request.user.username)


    try:
        check_already_like=like.objects.filter(PostID=Postid,Userlike=user)

        if check_already_like.exists():
            check_already_like.delete()
            status=False

        else:
            like.objects.create(PostID=Postid,Userlike=user)
            status=True

    except User.DoesNotExist:
            return HttpResponse(status=204) 

    return JsonResponse({"data": status})  


@login_required(login_url="signin")
def user_like_status(request):

    postid= request.GET.get('postid')

    user=User.objects.get(username=request.user.username)
    Postid=post.objects.get(id=postid)
    

    try:
        check_already_like=like.objects.filter(PostID=Postid,Userlike=user)

        if check_already_like.exists():
            status=True
        
        else:
            status=False

    except User.DoesNotExist:
            return HttpResponse(status=204) 
  
    return JsonResponse({"data": status})  


@login_required(login_url="signin")
def user_save(request):

    postid= request.GET.get('postid')
    print(post_upload)
    Postid=post.objects.get(id=postid)
    user=User.objects.get(username=request.user.username)


    try:
        check_already_saved=saved.objects.filter(PostID=Postid,UserSaved=user)

        if check_already_saved.exists():
            check_already_saved.delete()
            status=False

        else:
            saved.objects.create(PostID=Postid,UserSaved=user)
            status=True

    except User.DoesNotExist:
            return HttpResponse(status=204) 

    return JsonResponse({"data": status})  


@login_required(login_url="signin")
def user_save_status(request):

    postid= request.GET.get('postid')

    user=User.objects.get(username=request.user.username)
    Postid=post.objects.get(id=postid)
    

    try:
        check_already_saved=saved.objects.filter(PostID=Postid,UserSaved=user)

        if check_already_saved.exists():
            status=True
        
        else:
            status=False

    except User.DoesNotExist:
            return HttpResponse(status=204) 
  
    return JsonResponse({"data": status})  

@login_required(login_url="signin")
def saved_page(request):
    user=User.objects.get(username=request.user.username)
    user_profile=profile.objects.get(User=user)
    saved_users=saved.objects.filter(UserSaved=user)

    followingcount=follow.objects.filter(User=user).count()
    followercount=follow.objects.filter(Following=user).count()


    saved_post=[]
    saved_post_media=[]

    for saved_user in saved_users:

        saved_post += post.objects.filter(User=saved_user.PostID.User)

    for i in saved_post:
        
        saved_post_media +=postmedia.objects.filter(PostID=i)
    
    saved_post.reverse()
    return render(request,"profile\profile.html",{"user_profile":user_profile,
                                            "postdetails":saved_post,
                                            "postmedias":saved_post_media,
                                            "followingcount":followingcount,
                                            "followercount":followercount
                                            })