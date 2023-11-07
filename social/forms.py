from django import forms
from .models import Message

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