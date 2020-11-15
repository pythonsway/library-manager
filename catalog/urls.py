from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(),
         name='catalog'),
    path('create/', views.BookCreatetView.as_view(),
         name='book-create'),
    path('update/<slug:slug>', views.BookUpdatetView.as_view(),
         name='book-update'),
    path('details/<slug:slug>', views.BookDetailView.as_view(),
         name='book-details'),
    path('delete/<slug:slug>', views.BookDeletetView.as_view(),
         name='book-delete'),
    path('import/', views.googel_search,
         name='google-search'),
    path('import/save/', views.google_save,
         name='google-save'),
    path('api-info/', views.api_info,
         name='api-info'),
    path('author-autocomplete/', views.AuthorAutocomplete.as_view(create_field='name'),
         name='author-autocomplete'),
    path('language-autocomplete/', views.LanguageAutocomplete.as_view(),
         name='language-autocomplete'),
]
