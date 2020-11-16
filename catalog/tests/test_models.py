from datetime import datetime

from django.test import TestCase

from catalog.models import Author, Book, Language


class LanguageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name='English', code='en')

    def test_name_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_code_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('code').verbose_name
        self.assertEquals(field_label, 'code')

    def test_name_max_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_code_max_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('code').max_length
        self.assertEquals(max_length, 2)


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(name='Joe Black')

    def test_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        title = 'Django? Is that Spanish?'
        author = Author.objects.create(name='Joe Black')
        pub_date = datetime.datetime(2010, 5, 17)
        isbn = 1111111111111
        pages_num = 999
        language = Language.objects.create(name='English', code='en')
        Book.objects.create(
            title=title,
            pub_date=pub_date,
            isbn=isbn,
            pages_num=pages_num,
            language=language)
        Book.objects.get(id=1).authors.add(author)

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_authors_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('authors').verbose_name
        self.assertEquals(field_label, 'authors')

    def test_pub_date_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('pub_date').verbose_name
        self.assertEquals(field_label, 'pub date')

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEquals(field_label, 'ISBN')

    def test_pages_num_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('pages_num').verbose_name
        self.assertEquals(field_label, 'pages num')

    def test_cover_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('cover').verbose_name
        self.assertEquals(field_label, 'cover')

    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEquals(field_label, 'language')

    def test_slug_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEquals(max_length, 150)

    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEquals(max_length, 13)

    def test_slug_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('slug').max_length
        self.assertEquals(max_length, 300)

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.get_absolute_url(),
                          '/catalog/details/django-is-that-spanish-999/')
