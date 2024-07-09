from django.db import models


class Product(models.Model):
    title = models.CharField()
    description = models.TextField()

    def __str__(self):
        return self.title
