from django import forms
from .models import Blog, BlogComment

class postform(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['image','captions']

        widgets = {
            "captions": forms.TextInput(attrs={'class':'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(postform, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'

class commentform(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['text']

        widgets = {
            "text": forms.TextInput(attrs={'class':'form-control'})
        }