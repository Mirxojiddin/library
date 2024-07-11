from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Book
from .forms import BookForm



class BookListView(View):
    def get(self, request):
        all_books = Book.objects.all()
        context = {'all_books': all_books}
        return render(request, 'books/book_list.html', context)


class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'books/book_detail.html', {'book': book})


class BookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'books/book_form.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('books:book_list')
        return render(request, 'books/book_form.html', {'form': form})


class BookUpdateView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
        return render(request, 'books/book_form.html', {'form': form, 'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:book_list')
        return render(request, 'books/book_form.html', {'form': form, 'book': book})


class BookDeleteView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'books/book_confirm_delete.html', {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return redirect('books:book_list')
