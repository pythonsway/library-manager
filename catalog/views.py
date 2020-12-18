import os
from ast import literal_eval
from io import BytesIO

import requests
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from PIL import Image

from .forms import BookForm, BookSearchForm, GoogleSearchForm
from .models import Author, Book, Language


def index(request):
    if request.user.is_authenticated:
        return redirect('catalog')
    return render(request, 'catalog/index.html')


def api_info(request):
    return render(request, 'catalog/api_info.html')


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = BookSearchForm(initial=self.request.GET)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(users=self.request.user)
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


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book


class BookCreatetView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    success_message = 'Book was created'

    def form_valid(self, form):
        form.instance.users.add(self.request.user)
        return super().form_valid(form)


class BookUpdatetView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm
    success_message = 'Book was updated'


class BookDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('catalog')
    success_message = 'Book was deleted'

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


@login_required
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


@login_required
def google_save(request):
    if request.method == 'POST':
        user = request.user
        value_book = request.POST.get('book')
        google_book = literal_eval(value_book)
        title = google_book.get('title')
        identifiers = google_book.get('industryIdentifiers', [])
        isbn = None
        for id in identifiers:
            if id.get('type') == 'ISBN_13':
                isbn = id.get('identifier')
        if existing_book := Book.objects.filter(isbn=isbn).first():
            if user in existing_book.users.all():
                messages.info(request, 'Book already added')
                book_created = False
            else:
                existing_book.users.add(user)
                messages.success(request, 'Book saved')
                book_created = True
        else:
            pages_num = google_book.get('pageCount')
            language_code = google_book.get('language')
            partial_date = google_book.get('publishedDate')
            if partial_date and len(partial_date) < 5:
                partial_date = f'{partial_date}-01-01'
            elif partial_date and len(partial_date) < 8:
                partial_date = f'{partial_date}-01'
            pub_date = partial_date
            n_book, book_created = Book.objects.get_or_create(
                title=title,
                pub_date=pub_date,
                isbn=isbn,
                pages_num=pages_num,
                language=Language.objects.get(code=language_code))
            n_book.users.add(user)
            authors = google_book.get('authors')
            if authors:
                for name in authors:
                    n_author, author_created = Author.objects.get_or_create(
                        name=name)
                    n_author.save()
                    n_book.authors.add(n_author)
            try:
                image_url = google_book.get('imageLinks', {}).get('thumbnail')
                img_name = f'{slugify(title)}.jpg'
                img_response = requests.get(image_url, stream=True)
                if img_response.status_code == requests.codes.ok:
                    img_obj = Image.open(img_response.raw)
                    img_io = BytesIO()
                    img_obj.save(img_io, 'JPEG')
                    img_file = ContentFile(img_io.getvalue())
                    n_book.cover.save(img_name, img_file, save=False)
                    n_book.save()
            except requests.exceptions.RequestException:
                messages.info(request, 'Book cover is not avaible')
            messages.success(request, 'Book saved')
        all_messages = messages.get_messages(request)
        messages_html = render_to_string(
            'includes/messages.html',
            {'messages': all_messages},
            request=request
        )
        data = {
            'messages_html': messages_html,
            'book_created': book_created,
        }
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
