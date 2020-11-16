import os
from ast import literal_eval

import requests
from dal import autocomplete
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import BookForm, BookSearchForm, GoogleSearchForm
from .models import Author, Book, Language


class BookListView(ListView):
    model = Book
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = BookSearchForm(initial=self.request.GET)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        title = self.request.GET.get('title')
        authors = self.request.GET.get('authors')
        language = self.request.GET.get('language')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if title:
            qs = qs.filter(title__icontains=title)
        if authors:
            qs = qs.filter(authors__name__icontains=authors)
        if language:
            qs = qs.filter(language__name__icontains=language)
        if date_from:
            qs = qs.filter(pub_date__gte=date_from)
        if date_to:
            qs = qs.filter(pub_date__lte=date_to)
        return qs


class BookDetailView(DetailView):
    model = Book


class BookCreatetView(SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    success_message = '"%(title)s" was created'


class BookUpdatetView(SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm
    success_message = '"%(title)s" was updated'


class BookDeleteView(SuccessMessageMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('catalog')
    success_message = '"%(title)s" was deleted'

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


def api_info(request):
    messages.success(request, 'Book saved')
    return render(request, 'catalog/api-info.html')


def google_search(request):
    if request.method == 'POST':
        form = GoogleSearchForm(request.POST)
        if form.is_valid():
            API_URL = os.environ.get(
                'GOOGLE_API', 'https://www.googleapis.com/books/v1/volumes')
            MAX_RESULTS = 40
            start_index = 0
            has_next = True
            google_books = []
            if request.POST.get('form-values'):
                form_values = request.POST.get('form-values')
                start_index = int(request.POST.get('start-index'))
            else:
                form_values = '+'.join(
                    f'{k}:{v}' for k, v in form.cleaned_data.items() if v)
            params = {'q': form_values, 'maxResults': MAX_RESULTS,
                      'startIndex': start_index, }
            response = requests.get(url=API_URL, params=params, )
            if response.status_code == requests.codes.ok:
                response_json = response.json()
                try:
                    google_books = [item['volumeInfo']
                                    for item in response_json['items']]
                except KeyError:
                    has_next = False
                start_index += MAX_RESULTS
            if request.POST.get('page'):
                search_html = render_to_string(
                    'catalog/includes/partial_importitem_list.html',
                    {'google_books': google_books},
                    request=request
                )
                data = {
                    'search_html': search_html,
                    'has_next': has_next,
                    'start_index': start_index,
                }
                return JsonResponse(data)
            context = {
                'form': form,
                'google_books': google_books,
                'form_values': form_values,
                'start_index': start_index,
            }
            return render(request, 'catalog/google_search.html', context)
    form = GoogleSearchForm()
    return render(request, 'catalog/google_search.html', {'form': form})


def google_save(request):
    if request.method == 'POST':
        value_book = request.POST.get('book')
        google_book = literal_eval(value_book)
        title = google_book.get('title')
        identifiers = google_book.get('industryIdentifiers', [])
        isbn = None
        for id in identifiers:
            if id.get('type') == 'ISBN_13':
                isbn = id.get('identifier')
        if Book.objects.filter(isbn=isbn).exists():
            messages.info(request, f'{title} already exists')
            return redirect('catalog')
        pages_num = google_book.get('pageCount')
        image_url = google_book.get('imageLinks', {}).get('thumbnail')
        img_name = title.replace(' ', '')
        image_path = None
        img_response = requests.get(image_url, stream=True)
        if img_response.status_code == requests.codes.ok:
            image_path = f'covers/{img_name}.jpg'
            with default_storage.open(image_path, 'wb+') as image_dest:
                for chunk in img_response.iter_content(chunk_size=128):
                    image_dest.write(chunk)
        language_code = google_book.get('language')
        partial_date = google_book.get('publishedDate')
        if partial_date and len(partial_date) < 5:
            partial_date = f'{partial_date}-01-01'
        pub_date = partial_date
        n_book, book_created = Book.objects.get_or_create(
            title=title,
            pub_date=pub_date,
            isbn=isbn,
            pages_num=pages_num,
            cover=image_path,
            language=Language.objects.get(code=language_code))
        authors = google_book.get('authors')
        if authors:
            for name in authors:
                n_author, author_created = Author.objects.get_or_create(
                    name=name)
                n_author.save()
                n_book.authors.add(n_author)
        data = {
            'book_created': book_created,
        }
        messages.success(request, 'Book saved')
        return JsonResponse(data)
    return redirect('catalog')


# django-autocomplete-light
class AuthorAutocomplete(autocomplete.Select2QuerySetView):
    # allow guests for creating new objects
    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Author.objects.all()
        authors = self.forwarded.get('authors', None)
        if authors:
            qs = qs.exclude(pk__in=authors)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class LanguageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Language.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
