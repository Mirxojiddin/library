from django.urls import path

from accounts.views import LoginView, RegisterView, LogoutView, ProfileView, ProfileEdit

app_name = 'accounts'

urlpatterns = [
	path('register', RegisterView.as_view(), name='register'),
	path('login', LoginView.as_view(), name='login'),
	path('logout', LogoutView.as_view(), name='logout'),
	path('profile', ProfileView.as_view(), name='profile'),
	path('profile_edit', ProfileEdit.as_view(), name='profile_edit'),


]