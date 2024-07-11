from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import re
from accounts.models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_photo',
                  'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("This field is required.")
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError("A user with that username already exists.")
        if not re.match(r'^\w+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError("This field is required.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise ValidationError("This field is required.")
        return last_name

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("The two password fields didn’t match.")
            if len(password1) < 8:
                raise ValidationError("This password is too short. It must contain at least 8 characters.")
            if not re.search(r'\d', password1):
                raise ValidationError("The password must contain at least one digit.")
            if not re.search(r'[A-Z]', password1):
                raise ValidationError("The password must contain at least one uppercase letter.")
            if not re.search(r'[a-z]', password1):
                raise ValidationError("The password must contain at least one lowercase letter.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
                raise ValidationError("The password must contain at least one special character.")
        return password2


class CustomUserUpdateForm(UserChangeForm):
    password = None  # Remove the password field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_photo']
