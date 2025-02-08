from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class IMAPAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    imap_server = models.CharField(max_length=255)
    imap_port = models.IntegerField(default=993)
    use_ssl = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class IMAPConfig:
        imap_timeout = 30
        imap_retry_count = 3
        imap_folder_blacklist = ['Trash', 'Spam', 'Junk']
        imap_batch_size = 100

    def __str__(self):
        return self.email

class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    imap_server = models.CharField(max_length=255, default='imap.gmail.com')
    imap_port = models.IntegerField(
        default=993,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(65535),
        ]
    )
    use_ssl = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Email Account"
        verbose_name_plural = "Email Accounts"