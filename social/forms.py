from django import forms
from .models import Message , Profile

class ProfileEdit(forms.ModelForm):
    profile_bio = forms.CharField(label="Bio" , widget=forms.Textarea(attrs={'class':'form-control bio-field', 'placeholder':'Profile Bio' , 'id': 'id_profile_bio' , 'maxlength':'160'}) , required=False )
    profile_location = forms.CharField(label="location" , widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Location'}) , required=False)
    profile_website = forms.CharField(label = "website" ,  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website'}), required=False)
    profile_image = forms.ImageField(label="Profile Picture" , required=False)
    background_image = forms.ImageField(label="Profile Background" , required=False)
    class Meta:
        model = Profile
        fields = ('profile_bio' , 'profile_location' , 'profile_website' , 'profile_image' , 'background_image' )


class MessageForm(forms.ModelForm):
    body = forms.CharField(required=True , 
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder":"What's happenning?!",
                                   "class":"form-control",
                                   "maxlength":"200",
                               }
                           ),
                           label="",
                           )
    
    class Meta:
        model = Message
        exclude = ("user" ,"likes" , )  
    def __init__(self, *args, **kwargs):
        parent_message = kwargs.pop('parent_message', None)
        super().__init__(*args, **kwargs)
        self.fields['parent_message'].widget = forms.HiddenInput()
        self.fields['parent_message'].initial = parent_message  