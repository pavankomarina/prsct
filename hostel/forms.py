from django import forms
from django.contrib.auth.models import User

from .models import Profile, Marks_card,Vote


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'college', 'course', 'photo']
        #fields = ['artist', 'album_title', 'genre', 'album_logo']


class MarkscardForm(forms.ModelForm):

    class Meta:
        model = Marks_card
        fields = ['semester', 'marks_card']
        #fields = ['song_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
class VoteForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['answer']

