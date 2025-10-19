from django.conf import settings
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)  # ISBN-13 expected, ensure uniqueness
    published_date = models.DateField(null=True, blank=True)
    copies_total = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["title", "author"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["author"]),
            models.Index(fields=["isbn"]),
        ]

    def __str__(self):
        return f"{self.title} — {self.author} ({self.isbn})"

    def save(self, *args, **kwargs):
        # Ensure copies_available never exceeds copies_total
        if self.copies_available > self.copies_total:
            self.copies_available = self.copies_total
        super().save(*args, **kwargs)


class Transaction(models.Model):
    STATUS_CHECKED_OUT = "checked_out"
    STATUS_RETURNED = "returned"
    STATUS_CHOICES = [
        (STATUS_CHECKED_OUT, "Checked out"),
        (STATUS_RETURNED, "Returned"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="transactions")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHECKED_OUT)
    checked_out_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-checked_out_at"]
        # Prevent a user from having more than one active (not returned) transaction for the same book
        constraints = [
            UniqueConstraint(
                fields=["user", "book"],
                condition=Q(returned_at__isnull=True),
                name="unique_active_user_book_transaction",
            )
        ]

    def __str__(self):
        return f"{self.user} — {self.book} [{self.status}]"
