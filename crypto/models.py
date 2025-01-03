from django.contrib.auth.models import User
from django.db import models


class CryptoRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.CharField(max_length=100)
    requested_at = models.DateTimeField(auto_now_add=True)
    response_data = models.JSONField()

    def __str__(self):
        return f"{self.cryptocurrency} - {self.user.username} at {self.requested_at}"
