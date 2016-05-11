"""
:Created: 5 April 2015
:Author: Lucas Connors

"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterAccountForm(UserCreationForm):

    email = forms.EmailField(required=True)
    subscribe_news = forms.BooleanField(required=False, label='Subscribe to general updates about PerDiem')

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(RegisterAccountForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EditNameForm(forms.ModelForm):

    invest_anonymously = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)


class ContactForm(forms.Form):

    INQUIRY_CHOICES = (
        ('Support', 'Support',),
        ('Feedback', 'Feedback',),
        ('General Inquiry',  'General Inquiry',),
    )

    inquiry = forms.ChoiceField(choices=INQUIRY_CHOICES)
    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea)
