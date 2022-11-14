from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django import forms 
from account.models import Profile


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)


    class Meta:
        model = User 
        fields = ('username', 'first_name','last_name','email', 'password1', 'password2')


class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Old Password'}))
    new_password1 = forms.CharField(max_length=50, widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter New Password'}))
    new_password2 = forms.CharField(max_length=50, widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat New Password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    

# class RestPasswordForm(PasswordResetForm):
#     email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email address.'}))
    
#     class Meta:
#         model = User 
#         fields = ('email',)


#     def __init__(self,*args, **kwargs):
#         super(RestPasswordForm, self).__init__(*args, **kwargs)
#         self.fields['email'].widget.attrs['class'] = 'form-control'



STATE =[
    ('Abia', 'Abia'),
    ('Bayelsa', 'Bayelsa'),
    ('Delta', 'Delta'),
    ('Edo', 'Edo'),
    ('Lagos', 'Lagos'),
]
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','email','phone','address','city','state','profile_img')
        widgets ={
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email Address'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Phone Number'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Address'}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter City'}),
            'state': forms.Select(attrs={'class':'form-control', 'placeholder':'Enter State'}, choices=STATE),
            'profile_img': forms.FileInput(attrs={'class':'form-control'})
        }
        