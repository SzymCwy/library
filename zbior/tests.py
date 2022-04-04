from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from .models import Book
import datetime
from django.urls import reverse
from .forms import Book_create_form, Book_update_form


def sample_book(title='Hobbit', author='Rowling', publish_date=datetime.date.today(), isbn='9781452156149',
                page_number=1, cover_link='https://www.sample.pl', publish_language='pl'):
    return Book.objects.create(title=title, author=author, publish_date=publish_date, ISBN_Number=isbn,
                               number_of_pages=page_number, cover_link=cover_link, publish_language=publish_language)


def sample_form_create(title='Hobbit', author='Rowling', publish_date=datetime.date.today(), isbn='9780871785411',
                       page_number=1, cover_link='https://wwww.sample.pl', publish_language='pl'):
    pay_load = {
        'title': title,
        'author': author,
        'publish_date': publish_date,
        'ISBN_Number': isbn,
        'number_of_pages': page_number,
        'cover_link': cover_link,
        'publish_language': publish_language,
    }
    return pay_load


def sample_form_update(title='Hobbit', author='Rowling', publish_date=datetime.date.today(), isbn='9781452156149',
                       page_number=1, cover_link='https://siema.pl', publish_language='pl'):
    pay_load = {
        'title': title,
        'author': author,
        'publish_date': publish_date,
        'ISBN_Number': isbn,
        'number_of_pages': page_number,
        'cover_link': cover_link,
        'publish_language': publish_language,
    }
    return pay_load


class BookTestCase(TestCase):

    def test_create_book(self):
        sample_book()
        self.assertTrue(Book.objects.all().exists())

    def test_create_book_wrong_date(self):
        with self.assertRaises(ValidationError):
            pub_date = datetime.date.today() + datetime.timedelta(days=1)
            book = sample_book(publish_date=pub_date)
            book.full_clean()

    def test_create_book_wrong_isbn(self):
        with self.assertRaises(ValidationError):
            isbn = '123654945'
            book = sample_book(isbn=isbn)
            book.full_clean()

    def test_create_book_invalid_url(self):
        with self.assertRaises(ValidationError):
            cover_link = 'l'
            book = sample_book(cover_link=cover_link)
            book.full_clean()

    def test_book_str(self):
        book = sample_book()
        self.assertEqual(str(book), f'{book.title} - {book.author}')


class Api_test(TestCase):

    def test_list(self):
        sample_book()
        c = Client()
        response = c.get(reverse(viewname='book-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertContains(response, 'Hobbit')

    def test_list_queryset_search(self):
        c = Client()
        sample_book()
        response = c.get(reverse(viewname='book-list'), {'search': 'Hobbit'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertContains(response, 'Hobbit')

    def test_list_queryset_search_date(self):
        c = Client()
        sample_book()
        response = c.get(reverse(viewname='book-list'),
                         {'search': 'Hobbit', 'date_from': (datetime.date.today() - datetime.timedelta(days=1000)),
                          'date_till': datetime.date.today()})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertContains(response, 'Hobbit')

    def test_list_wrong_date(self):
        c = Client()
        sample_book()
        response = c.get(reverse(viewname='book-list'),
                         {'search': 'Hobbit', 'date_from': '11-11-200'})
        self.assertTemplateUsed(response, 'error.html')

    def test_list_queryset_date(self):
        c = Client()
        sample_book()
        response = c.get(reverse(viewname='book-list'),
                         {'date_from': (datetime.date.today() - datetime.timedelta(days=1000)),
                          'date_till': datetime.date.today()})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertContains(response, 'Hobbit')

    def test_list_queryset_date_range(self):
        c = Client()
        response = c.get(reverse(viewname='book-list'),
                         {'date_till': (datetime.date.today() - datetime.timedelta(days=1000)),
                          'date_from': datetime.date.today()})
        self.assertTemplateUsed(response, 'error.html')

    def test_import(self):
        c = Client()
        response = c.get(reverse(viewname='book-import'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_import.html')

    def test_import_query(self):
        c = Client()
        response = c.get(reverse(viewname='book-import'), {'import': 'rToaogEACAAJ'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][0], reverse(viewname='book-list'))
        self.assertTrue(Book.objects.all().exists())
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertContains(response, 'Hobbit czyli Tam i z powrotem')

    def test_import_search(self):
        c = Client()
        response = c.get(reverse(viewname='book-import'), {'search': 'Ukryty utwór'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_import.html')
        self.assertContains(response, 'Walentina Nazarowa')


class Form_test_create(TestCase):
    def test_form_date(self):
        form = Book_create_form(
            data=sample_form_create(publish_date=datetime.date.today() + datetime.timedelta(days=1)))
        self.assertEqual(
            form.errors['publish_date'], ['The book publish date cannot be in the future!'])

    def test_form_url(self):
        form = Book_create_form(data=sample_form_create(cover_link='p'))
        self.assertEqual(
            form.errors['cover_link'], ['Enter a valid URL.'])

    def test_form_isbn(self):
        form = Book_create_form(data=sample_form_create(isbn='123'))
        self.assertEqual(
            form.errors['ISBN_Number'], ['Incorrect ISBN'])

    def test_form_isbn_control(self):
        form = Book_create_form(data=sample_form_create(isbn='9781503514118'))
        self.assertEqual(
            form.errors['ISBN_Number'], ['ISBN control sum incorrect!'])

    def test_form_book_exists_isbn(self):
        sample_book()
        form = Book_create_form(data=sample_form_create(isbn='9781452156149'))
        self.assertEqual(form.errors['ISBN_Number'], ['That Book already exists in your library!'])

    def test_form_book_exists(self):
        sample_book()
        form = Book_create_form(data=sample_form_create(author='Rowling', title='Hobbit', isbn='1231231233'))
        self.assertEqual(form.errors['__all__'], ['That Book already exists in your library!'])


class API_test(TestCase):

    def test_api_get(self):
        sample_book()
        c = Client()
        response = c.get(reverse(viewname='book-api'))
        self.assertContains(response, 'Hobbit')
        self.assertEqual(response.status_code, 200)

    def test_api_search(self):
        sample_book()
        c = Client()
        response = c.get(reverse(viewname='book-api'), {'search': 'Hobbit'})
        self.assertContains(response, 'Hobbit')
        self.assertEqual(response.status_code, 200)

    def test_api_date(self):
        sample_book()
        c = Client()
        response = c.get(reverse(viewname='book-api'), {'date_from': datetime.date.today(),
                                                        'date_till': datetime.date.today()})
        self.assertContains(response, 'Hobbit')
        self.assertEqual(response.status_code, 200)

    def test_api_invalid_date(self):
        sample_book()
        c = Client()
        response = c.get(reverse(viewname='book-api'), {'date_from': '2020-13-13',
                                                        'date_till': datetime.date.today()})
        self.assertEqual(response.status_code, 400)

    def test_api_invalid_date_range(self):
        sample_book()
        c = Client()
        response = c.get(reverse(viewname='book-api'),
                         {'date_from': datetime.date.today(),
                          'date_till': datetime.date.today() - datetime.timedelta(days=1)})
        self.assertEqual(response.status_code, 400)


class Form_test_update(TestCase):

    def test_update_form(self):
        book = sample_book()
        book2 = sample_form_update(title='Hobbit2', isbn='9781503514119')
        form = Book_update_form(data=book2, instance=book)
        self.assertTrue(form.is_valid())
        form.save(commit=True)
        self.assertTrue(Book.objects.filter(title='Hobbit2'))

    def test_update_form_same_isbn(self):
        book2 = sample_book(title='Hobbit2', isbn='9781503514119')
        book3 = sample_form_update(title='Hobbit2', isbn='9781452156149')
        form = Book_update_form(data=book3, instance=book2)
        self.assertFalse(form.is_valid())

    def test_update_form_wrong_isbn(self):
        with self.assertRaises(ValueError):
            book = sample_book()
            book2 = sample_form_update(title='Hobbit2', isbn='97815032514119')
            form = Book_update_form(data=book2, instance=book)
            form.save(commit=True)

    def test_update_form_wrong_date(self):
        with self.assertRaises(ValueError):
            book = sample_book()
            book2 = sample_form_update(title='Hobbit2', isbn='97815032514119', publish_date=datetime.date(2000, 13, 11))
            form = Book_update_form(data=book2, instance=book)
            form.save(commit=True)
