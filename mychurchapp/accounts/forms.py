from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'contact_number')

class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields a user has.
    """
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


from django import forms
from .models import Profile

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture',)
