from django import forms
from .models import Message , Profile

class ProfileEdit(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture" , required=False)
    background_image = forms.ImageField(label="Profile Background" , required=False)
    class Meta:
        model = Profile
        fields = ('profile_image' , 'background_image' )


class MessageForm(forms.ModelForm):
    body = forms.CharField(required=True , 
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder":"Enter your message",
                                   "class":"form-control",
                               }
                           ),
                           label="",
                           )
    
    class Meta:
        model = Message
        exclude = ("user" , )    