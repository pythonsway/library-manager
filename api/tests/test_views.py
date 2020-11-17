from datetime import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from catalog.models import Author, Book, Language


class BookListApiTest(APITestCase):

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

    def test_api_url_exists_at_desired_location(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        url = reverse('api-books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
