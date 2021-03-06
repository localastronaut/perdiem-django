"""
:Created: 19 March 2016
:Author: Lucas Connors

"""

from django import forms


class CoordinatesFromAddressForm(forms.Form):

    address = forms.CharField()


class ArtistApplyForm(forms.Form):

    artist_name = forms.CharField(label='Artist / Band Name')
    genre = forms.CharField()
    hometown = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'We started playing music because...',}))
    campaign_reason = forms.CharField(label='Why are you raising money?', widget=forms.Textarea(attrs={'placeholder': 'We are trying to record our album...',}))
    campaign_expenses = forms.CharField(label='What do you need the money for?', widget=forms.Textarea(attrs={'placeholder': 'Mixing, mastering, studio time, etc...',}))
    facebook = forms.URLField(required=False, widget=forms.TextInput(attrs={'placeholder': 'http://',}))
    twitter = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '@',}))
    instagram = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '@',}))
    music_link = forms.URLField(label='Link to music', widget=forms.TextInput(attrs={'placeholder': 'http://',}))
    terms = forms.BooleanField(label='Terms & Conditions', help_text='I have read and agree to the Terms & Conditions')
