import datetime


def date_validate(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        return None


def date_from_universal(date):
    mapping = {None: datetime.date(1800, 1, 1), '': datetime.date(1800, 1, 1)}
    correct_date = mapping[date] if date in mapping else date_validate(date)
    return correct_date


def date_till_universal(date):
    mapping = {None: datetime.date.today(), '': datetime.date.today()}
    correct_date = mapping[date] if date in mapping else date_validate(date)
    return correct_date


def correct_date_range(date_from, date_till):
    if date_from > date_till:
        return True


def book_import_query(book):
    authors = ' '.join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else ''
    book_dict = {
        'id': book['id'],
        'title': book['volumeInfo']['title'],
        'author': authors,
        'publish_date': book['volumeInfo']['publishedDate'] if 'publishedDate' in book['volumeInfo'] else '',
        'ISBN': book['volumeInfo']['industryIdentifiers'][0]['identifier'] if 'industryIdentifiers' in book[
            'volumeInfo'] else '',
        'cover_link': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else '',
        'language': book['volumeInfo']['language'] if 'language' in book['volumeInfo'] else '',
        'pages': book['volumeInfo']['pageCount'] if 'pageCount' in book['volumeInfo'] else 0,
    }
    return book_dict


def order_list(queryset):
    mapping = {'Author_ascending': 'author', 'Author_descending': '-author', 'Title_ascending': 'title',
               'Title_descending': '-title', 'Language_ascending': 'publish_language',
               'Language_descending': '-publish_language', 'Date_ascending': 'publish_date',
               'Date_descending': '-publish_date', '': 'author', None: 'author'}
    return mapping[queryset]


