from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class SubCategory(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Book(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	author = models.CharField(max_length=100)
	year = models.IntegerField()
	pages = models.IntegerField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
	sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
	url = models.URLField(null=True, blank=True)
	file = models.FileField(upload_to='books/', null=True, blank=True)
	size = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	isbn = models.CharField(max_length=20, null=True, blank=True)
	image = models.ImageField(upload_to='books/', null=True, blank=True, default='cover-photo.png')

	def __str__(self):
		return self.title


class BookShowed(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	created_at = models.DateField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return f'{self.book}'


class BookDownloaded(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.book}'

	class Meta:
		unique_together = ('book', 'user')


class OrderBook(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	book_name = models.CharField(max_length=100)
	description = models.TextField()
	author = models.CharField(max_length=100)
	status = models.BooleanField(default=False)
	created_at = models.DateField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return f'{self.book_name}'


class SendBook(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	book_name = models.CharField(max_length=100)
	description = models.TextField()
	author = models.CharField(max_length=100)
	file = models.FileField(upload_to='books/', null=True, blank=True)
	url = models.URLField(null=True, blank=True)
	status = models.BooleanField(default=False)
	created_at = models.DateField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return f'{self.book_name}'
