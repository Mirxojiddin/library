from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, FileResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from .models import Book, Category, BookDownloaded, BookShowed, OrderBook, SendBook
from .forms import BookForm, OrderBookForm, SendBookForm
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_latest_books():
    latest_books = Book.objects.order_by('-created_at')[:10]
    return latest_books


class BookListView(View):
    def get(self, request):
        categories = Category.objects.all()
        book_list = Book.objects.annotate(showed_count=Count('bookshowed')).order_by('-showed_count')

        query_params = request.GET
        latest_books = get_latest_books()
        title = query_params.get('title', None)
        author = query_params.get('author', None)
        year = query_params.get('year', None)
        isbn = query_params.get('isbn', None)

        if title:
            book_list = book_list.filter(title__icontains=title)
        if author:
            book_list = book_list.filter(author__icontains=author)
        if year:
            book_list = book_list.filter(year=year)
        if isbn:
            book_list = book_list.filter(isbn__icontains=isbn)

        paginator = Paginator(book_list, 6)

        page = request.GET.get('page')
        try:
            all_books = paginator.page(page)
        except PageNotAnInteger:

            all_books = paginator.page(1)
        except EmptyPage:
            all_books = paginator.page(paginator.num_pages)

        query_params = query_params.dict()
        if 'page' in query_params:
            del query_params['page']
        encoded_query_params = urlencode(query_params)
        context = {
            'all_books': all_books,
            'query_params': encoded_query_params,
            'categories': categories,
            'last_books': latest_books
        }
        return render(request, 'books/book_list.html', context)


class CategoryBookListView(View):
    def get(self, request, category_id):
        categories = Category.objects.all()
        book_list = Book.objects.annotate(showed_count=Count('bookshowed')).order_by('-showed_count').filter(category_id=category_id)

        query_params = request.GET

        title = query_params.get('title', None)
        author = query_params.get('author', None)
        year = query_params.get('year', None)
        isbn = query_params.get('isbn', None)
        latest_books = get_latest_books()
        if title:
            book_list = book_list.filter(title__icontains=title)
        if author:
            book_list = book_list.filter(author__icontains=author)
        if year:
            book_list = book_list.filter(year=year)
        if isbn:
            book_list = book_list.filter(isbn__icontains=isbn)

        paginator = Paginator(book_list, 6)

        page = request.GET.get('page')
        try:
            all_books = paginator.page(page)
        except PageNotAnInteger:

            all_books = paginator.page(1)
        except EmptyPage:
            all_books = paginator.page(paginator.num_pages)

        query_params = query_params.dict()
        if 'page' in query_params:
            del query_params['page']
        encoded_query_params = urlencode(query_params)
        context = {
            'all_books': all_books,
            'query_params': encoded_query_params,
            'categories': categories,
            'last_books': latest_books
        }
        return render(request, 'books/book_list.html', context)


class BookDetailView(View):
    def get(self, request, pk):

        categories = Category.objects.all()
        book = get_object_or_404(Book, pk=pk)
        user = request.user
        if user.is_authenticated:
            BookShowed.objects.create(book=book, user=user)
        latest_books = get_latest_books()
        context = {
            'book': book,
            'categories': categories,
            'last_books': latest_books
        }
        return render(request, 'books/book_detail.html', context)


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


class DownloadBookView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        user = request.user
        if not book.file:
            raise Http404("Book file not found.")
        BookDownloaded.objects.create(user=user, book=book)
        response = FileResponse(book.file.open('rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{book.file.name}"'

        return response


class OrderBookView(LoginRequiredMixin, View):
    def get(self, request):
        form = OrderBookForm()
        return render(request, 'books/order_book.html', {'form': form})

    def post(self, request):
        form = OrderBookForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, 'Sizning habaringiz adminga yuborildi')
            return redirect('books:book_list')
        return render(request, 'books/order_book.html', {'form': form})
    

class SendBookView(LoginRequiredMixin, View):
    def get(self, request):
        form = SendBookForm()
        return render(request, 'books/send_book.html', {'form': form})

    def post(self, request):
        form = OrderBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            messages.success(request, 'Sizning habaringiz adminga yuborildi')
            return redirect('books:book_list')
        return render(request, 'books/send_book.html', {'form': form})
    

class OrderedBookView(LoginRequiredMixin, View):
    def get(self, request):
        orders = OrderBook.objects.all()
        return render(request, 'books/ordered_book.html', {'orders':orders})


class SendedBookView(LoginRequiredMixin, View):
    def get(self, request):
        sends = SendBook.objects.all()
        return render(request, 'books/sended_book.html', {'sends':sends})


class SendedBookDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = SendBook.objects.get(pk=pk)
        return render(request, 'books/sended_book_detail.html', {'book':book})
    

class OrderedBookDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = OrderBook.objects.get(pk=pk)
        return render(request, 'books/ordered_book_detail.html', {'book':book})
