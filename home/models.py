from django.db import models

class HomeContent(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.TextField(blank=True)

    def __str__(self):
        return self.title
