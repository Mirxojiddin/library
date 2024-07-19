from django.contrib import admin
from books.models import Book, Category, SubCategory, BookShowed

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(BookShowed)