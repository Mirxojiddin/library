from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'year', 'pages', 'category', 'sub_category', 'url', 'file', 'size']
