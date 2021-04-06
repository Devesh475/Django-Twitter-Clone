from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import userform
from django.contrib.auth.models import User

class createUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

        widgets = {
            "username": forms.TextInput(attrs={'class':'form-control'}),
            "email": forms.TextInput(attrs={'class':'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(createUser, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class profileform(forms.ModelForm):
    class Meta:
        model = userform
        fields = ['firstName','lastName','gender','profileImage','contactNumber','address','bio']

        widgets = {
            "firstName": forms.TextInput(attrs={'class':'form-control'}),
            "lastName": forms.TextInput(attrs={'class':'form-control'}),
            "contactNumber": forms.TextInput(attrs={'class':'form-control'}),
            "address": forms.TextInput(attrs={'class':'form-control'}),
            "bio": forms.TextInput(attrs={'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(profileform, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['profileImage'].widget.attrs['class'] = 'form-control'
    
class resetpassword(forms.Form):
    newpassword = forms.PasswordInput()
    newpasswordconf = forms.PasswordInput()
    