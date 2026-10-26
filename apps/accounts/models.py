from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager

class User(AbstractUser):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
        (BLOCKED, "Blocked"),
    )
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=20, default=ACTIVE, choices=STATUS_CHOICES)
    otp = models.IntegerField(null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    forgot_password_token = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"#{self.pk} - {self.email}"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['is_superuser', '-created_at']
