from django import forms



# class user_signup(forms.ModelForm):
#     Fullname=forms.CharField(max_length=60)
#     email = forms.EmailField(required=True)
    
#     class Meta:
#         model = User
#         fields = ['username','email','password']
#         # exclude = ['owner_comment']
#         labels = {
            
#             "username": "UserName",
#             "email": "Email",
#             "password": "Password"
#         }
#         # error_messages = {
#         #     "username": {
#         #       "required": "Your name must not be empty!",
#         #       "max_length": "Please enter a shorter name!"
#         #     }
#         # }


class signup_form(forms.Form):

    Email = forms.EmailField(required=True)
    Fullname=forms.CharField(max_length=60)
    Username=forms.CharField(max_length=60)
    Password=forms.CharField(max_length=60)
