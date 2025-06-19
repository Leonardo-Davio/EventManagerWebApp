from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

class Motorcycle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='motorcycles')
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(blank=True, null=True)
    displacement = models.PositiveIntegerField(blank=True, null=True, help_text="Cilindrata in cc")
    notes = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.owner.username}"
