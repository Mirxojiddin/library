from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from accounts.models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_photo',
                  'password1', 'password2']


class CustomUserUpdateForm(UserChangeForm):
    password = None  # Remove the password field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_photo']
