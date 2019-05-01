from django import forms
from .models import Note

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ValidationError


class VenueSearchForm(forms.Form):
    search_name = forms.CharField(label='Venue Name', max_length=200)


class ArtistSearchForm(forms.Form):
    search_name = forms.CharField(label='Artist Name', max_length=200)


class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text')

# To edit notes, extend User Change Form into class Edit Note Form
class EditNoteForm(UserChangeForm):

    # use Note Meta data and meta fields
    class Meta:
        model = Note
        fields = ('title', 'text')

    # save the editable fields, and commit the changes
    def save(self, commit=True):
        note = super(EditNoteForm, self).save(commit=False)
        note.title = self.cleaned_data['title']
        note.text = self.cleaned_data['text']

        # if commit doesn't throw an error, save the note
        if commit:
            note.save()

# extend the User Change Form to Edit the User Profile
class EditProfileForm(UserChangeForm):

    # use the User model meta data
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    # save the editable changes for self.super User, for fields allowed to be edited. Notice password is excluded due
    # to Django password requirements
    # commit the changes to the form template
    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def clean_username(self):

        username = self.cleaned_data['username']

        if not username:
            raise ValidationError('Please enter a username')

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('A user with that username already exists')

        return username


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError('Please enter your first name')

        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError('Please enter your last name')

        return last_name


    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Please enter an email address')

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email address already exists')

        return email


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user
