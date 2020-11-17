from datetime import datetime, timedelta

from django.test import TestCase

from catalog.forms import BookForm, BookSearchForm


class BookFormTest(TestCase):

    def test_pub_date_in_future(self):
        date = datetime.now() + timedelta(day=1)
        form = BookForm(data={'pub_date': date})
        self.assertFalse(form.is_valid())


class BookSearchFormTest(TestCase):

    def test_date_from_in_future(self):
        date = datetime.now() + datetime.timedelta(day=1)
        form = BookSearchForm(data={'date_from': date})
        self.assertFalse(form.is_valid())

    def test_date_to_in_future(self):
        date = datetime.now() + datetime.timedelta(day=1)
        form = BookSearchForm(data={'date_to': date})
        self.assertFalse(form.is_valid())
