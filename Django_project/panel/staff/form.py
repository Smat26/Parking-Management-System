
from django import forms

class UserForm(forms.Form):
    username = forms.CharField(
    	widget=forms.TextInput(attrs={
    		'placeholder':'Username',

    		})
    	)
    password = forms.CharField(widget=forms.PasswordInput(
    		attrs={
    		'placeholder':'Password',

    		})
    	)


