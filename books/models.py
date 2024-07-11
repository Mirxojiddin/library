from django.db import models


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
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
	url = models.URLField(null=True, blank=True)
	file = models.FileField(upload_to='books/', null=True, blank=True)
	size = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.title
