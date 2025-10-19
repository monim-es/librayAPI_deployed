from django.contrib import admin
from .models import Book, Transaction


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "copies_total", "copies_available")
    search_fields = ("title", "author", "isbn")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "status", "checked_out_at", "returned_at")
    list_filter = ("status",)
    search_fields = ("user__username", "book__title", "book__isbn")
