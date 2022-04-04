from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import Book_update_form, Book_create_form
from .serializers import Book_serializer
import requests
from dateutil import parser
from .utils import date_from_universal, date_till_universal, correct_date_range, book_import_query, order_list
from rest_framework.views import APIView
from rest_framework.response import Response


def books_list_view(request):
    queryset = None
    if request.method == 'GET':
        date_till = date_till_universal(request.GET.get('date_till'))
        date_from = date_from_universal(request.GET.get('date_from'))

        if date_till is None or date_from is None:
            return render(request, 'error.html', {'error': 'Wrong query - wrong date format'})

        if correct_date_range(date_from, date_till):
            return render(request, 'error.html', {'error': 'Wrong query - date_from < date_till'})

        if request.GET.get('search') is None:
            """If there are no query params for searching the view is displaying list of all books"""
            queryset = Book.objects.all()

        elif request.GET.get('search') is not None:
            """If search contains any information"""
            queryset = Book.objects.filter(
                Q(title__contains=request.GET.get('search')) |
                Q(author__contains=request.GET.get('search')) |
                Q(publish_language=request.GET.get('search'))).intersection(Book.objects.filter(
                  publish_date__range=[date_from, date_till]))

        context = {
            'object_list': queryset.order_by(order_list(request.GET.get('sort')))
        }
        return render(request, 'book_list.html', context)


def books_edit(request, my_id):
    obj = get_object_or_404(Book, id=my_id)
    obj2 = get_object_or_404(Book, id=my_id)
    form = Book_update_form(instance=obj, data=request.POST or None)
    if request.method == 'POST':
        Book.delete(obj)
        if form.is_valid():
            form.save()
            print(obj)
        else:
            Book.save(obj2)
    context = {
        'form': form
    }
    return render(request, 'book_update.html', context)


def books_create(request):
    form = Book_create_form(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'book_update.html', context)


def books_delete(request, my_id):
    obj = get_object_or_404(Book, id=my_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('/')
    return render(request, 'book_delete.html')


def book_import(request):
    api_key = 'AIzaSyCdeIfC04XTzYUlad2xedyJ6eEGFu2jIVc'
    if request.GET.get('import') is not None:
        import_book = request.GET.get('import')
        book_query = requests.get(f'https://www.googleapis.com/books/v1/volumes/{import_book}').json()
        book_dict = book_import_query(book_query)
        if Book.objects.all().filter(ISBN_Number=book_dict['ISBN']).exists():
            return render(request, 'error.html', context={'error': 'This book already exists!'})
        else:
            imported_book = Book.objects.create(author=book_dict['author'], title=book_dict['title'],
                                                publish_date=parser.parse(book_dict['publish_date']),
                                                ISBN_Number=book_dict['ISBN'], cover_link=book_dict['cover_link'],
                                                number_of_pages=book_dict['pages'],
                                                publish_language=book_dict['language'])
            imported_book.save()
            return redirect('/')

    elif request.GET.get('search') is not None:
        books = []
        searched_phrase = request.GET.get('search')
        queries = {'q': searched_phrase, 'key': api_key}
        queryset = requests.get('https://www.googleapis.com/books/v1/volumes', params=queries).json()
        queryset = queryset['items']

        for book in queryset:
            book_dict = {
                'id': book['id'],
                'title': book['volumeInfo']['title'],
                'author': ' '.join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else '',
                'publish_date': book['volumeInfo']['publishedDate'] if 'publishedDate' in book['volumeInfo'] else '',
            }
            books.append(book_dict)
        context = {
            'books': books
        }
        return render(request, 'book_import.html', context)

    else:
        return render(request, 'book_import.html')


class Book_API(APIView):

    def get(self, request):
        date_till = date_till_universal(self.request.query_params.get('date_till'))
        date_from = date_from_universal(self.request.query_params.get('date_from'))

        if date_till is None or date_from is None:
            return Response(status=400)

        if correct_date_range(date_from, date_till):
            return Response(status=400)

        if self.request.query_params.get('search') is None:
            queryset = Book.objects.all()

        else:
            """If search contains any information"""
            queryset = Book.objects.filter(
                Q(title__contains=self.request.query_params.get('search')) |
                Q(author__contains=self.request.query_params.get('search')) |
                Q(publish_language=self.request.query_params.get('search'))).intersection(Book.objects.filter(
                  publish_date__range=[date_from, date_till]))
        serializer = Book_serializer(queryset, many=True)
        return Response(serializer.data)
