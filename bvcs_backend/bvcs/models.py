from django.db import models
from django.contrib.auth.models import User

class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "repositories"
        unique_together = [['user', 'name']]


class Commit(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="commits"
    )
    hash = models.CharField(max_length=64, unique=True)
    parent_hash = models.CharField(max_length=64, blank=True)
    blob_hash = models.CharField(max_length=64)
    message = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.repository.name} — {self.hash[:8]}"

    class Meta:
        ordering = ["-timestamp"]