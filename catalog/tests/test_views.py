from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from catalog.models import Author, Book, Language


class BookListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        books_number = 15
        pub_date = datetime(2010, 5, 17)
        isbn = 1111111111111
        pages_num = 999
        language = Language.objects.create(name='English', code='en')
        for idx in range(books_number):
            isbn += 1
            Book.objects.create(
                title=f'title {idx}',
                pub_date=pub_date,
                isbn=isbn,
                pages_num=pages_num,
                language=language)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['book_list']) == 10)

    def test_lists_all_books(self):
        response = self.client.get(f'{reverse("catalog")}?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['author_list']) == 5)


class BookCreatetViewTest(TestCase):

    def setUp(self):
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

    def test_uses_correct_template(self):
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_form.html')

    def test_redirects_to_detail_view_on_success(self):
        response = self.client.post(reverse('book-create'),
                                    {'title': 'Zero To One', })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalog/details/'))


class BookUpdateViewTest(TestCase):

    def setUp(self):
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

    def test_uses_correct_template(self):
        response = self.client.get(reverse('book-update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_form.html')

    def test_redirects_to_list_view_on_success(self):
        response = self.client.post(reverse('book-update'),
                                    {'title': 'Zero To One', })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalog/'))


class BookDeleteViewTest(TestCase):

    def setUp(self):
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

    def test_uses_correct_template(self):
        response = self.client.get(reverse('book-delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_confirm_delete.html')

    def test_redirects_to_list_view_on_success(self):
        response = self.client.post(reverse('book-delete'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalog/'))


class ApiInfoViewTest(TestCase):

    def test_uses_correct_template(self):
        response = self.client.get(reverse('api-info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/api-info.html')


class GoogleSearchViewTest(TestCase):

    def test_uses_correct_template(self):
        response = self.client.get(reverse('google-search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/google_search.html')


class GoogleSaveViewTest(TestCase):

    def setUp(self):
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

    def test_redirects_to_detail_view_if_exists(self):
        response = self.client.post(reverse('google-save'),
                                    {'isbn': '1111111111111', })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalog/'))
