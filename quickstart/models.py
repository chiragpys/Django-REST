from django.db import models


# Create your models here.

class Snippet(models.Model):
    created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created']
