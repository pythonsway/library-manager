from catalog.models import Book
from rest_framework import generics

from .filters import BookFilter
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """List all books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
