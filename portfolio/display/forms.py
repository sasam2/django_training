from django import forms

class PosteditForm(forms.Form):

    title = forms.CharField(label='Title')
    content = forms.CharField(label='Content', widget=forms.Textarea())


class SignupForm(forms.Form):

    username = forms.CharField(label='User name', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), required=True)
