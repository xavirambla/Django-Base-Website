from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class User_Form(forms.ModelForm):

    username  = forms.CharField(help_text="") #quitamos el mensaje pq era muy largo 
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')

    def clean_username(self):
        data = self.cleaned_data['username']
        #check name not is empty
        if len(data)<3:
            raise  ValidationError(_('Invalid username - field too short '))    
        # Remember to always return the cleaned data.
        return data



