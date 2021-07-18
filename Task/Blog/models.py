from datetime import datetime
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.author}'s ({self.title}) from _{self.posted_date}_"
