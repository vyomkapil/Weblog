from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import Post


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label = "Email", required=True)
    first_name = forms.CharField(label = "First name", required = True )
    last_name = forms.CharField(label = "Last name", required = True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2" )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        data = self.cleaned_data

        user = super(RegistrationForm, self).save()
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'cover_photo', 'post_text')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))