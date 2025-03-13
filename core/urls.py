from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     path("signup",views.signup_page,name='signup'), 
     path("checkuser/",views.check_username,name="checkuser"),
     path("gmail/",views.check_gmail,name="checkgmail"),
     path("signin",views.signin_page,name="signin"),
     path("setting",views.setting_page,name="setting"),
     path("",views.home_page,name="home"),
     path("logout/",views.logout_page,name="logout"),
     path("profilePhoto/",views.profile_photo_change,name="profile_change"),
     path("usernamechange/",views.username_edit_page,name="usernamechange"),
     path("post",views.post_upload,name="postupload"),
     path("profile/<str:username>",views.profile_page,name="profile"),
     path("comment_send/<str:username> <int:postid>",views.comment_send_model,name="comment_send"),
     path("follow_count/",views.follow_count ,name="follow"),
     path("follow_status/",views.follow_status,name="follow_status"),
     path("profile/<str:username>/following",views.following_page,name="following_page"),
     path("profile/<str:username>/follower",views.follower_page,name="follower_page"),
     path("comment/",views.get_comment_model,name="getcomment"),
     path("user_like/",views.user_like,name="user_like"),
     path("user_like_status/",views.user_like_status,name="user_like_status"),
     path("user_save/",views.user_save,name="user_save"),
     path("user_save_status/",views.user_save_status,name="user_save_status"),
     path("saved_page/",views.saved_page,name="saved_page"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
