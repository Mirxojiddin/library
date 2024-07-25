from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	USER_TYPES = (
		('student', 'Student'),
		('librarian', 'Librarian'),
	)
	username = models.CharField('username', max_length=30, unique=True)
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	user_photo = models.ImageField(default="default_photo.jpg")
	status = models.CharField(max_length=10, choices=USER_TYPES, default='student')

	def __str__(self):
		return self.username

	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"

	def can_add_book(self):
		return self.status == 'librarian'

	def can_order_book(self):
		return self.status == 'student'
