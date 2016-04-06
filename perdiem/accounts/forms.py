"""
:Created: 5 April 2015
:Author: Lucas Connors

"""

from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterAccountForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(RegisterAccountForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
