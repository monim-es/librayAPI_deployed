from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction as db_transaction
from django.utils import timezone
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer
from .permissions import IsAdminOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

class TransactionViewSet(viewsets.ModelViewSet):
    """
    Handles checkout and return of books
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own transactions
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='checkout')
    def checkout(self, request, pk=None):
        user = request.user
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if book.copies_available < 1:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        if Transaction.objects.filter(user=user, book=book, returned_at__isnull=True).exists():
            return Response({"error": "You already have this book checked out"}, status=status.HTTP_400_BAD_REQUEST)

        with db_transaction.atomic():
            book.copies_available -= 1
            book.save()
            txn = Transaction.objects.create(user=user, book=book)
            serializer = TransactionSerializer(txn)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='return')
    def return_book(self, request, pk=None):
        user = request.user
        try:
            txn = Transaction.objects.get(user=user, book_id=pk, returned_at__isnull=True)
        except Transaction.DoesNotExist:
            return Response({"error": "No active checkout found for this book"}, status=status.HTTP_400_BAD_REQUEST)

        with db_transaction.atomic():
            txn.status = Transaction.STATUS_RETURNED
            txn.returned_at = timezone.now()
            txn.save()

            book = txn.book
            book.copies_available += 1
            book.save()

            serializer = TransactionSerializer(txn)
            return Response(serializer.data, status=status.HTTP_200_OK)
