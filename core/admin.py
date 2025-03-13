from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import  profile ,post ,postmedia,comment,follow,like,saved

# Customize UserAdmin to show ID
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "date_joined", "is_staff")
    ordering = ("id",) 


# Unregister default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)




class Profile_readonly(admin.ModelAdmin):
    readonly_fields=('User',)

admin.site.register(profile, Profile_readonly)


admin.site.register(post)
admin.site.register(postmedia)
admin.site.register(comment)
admin.site.register(follow)
admin.site.register(like)
admin.site.register(saved)
