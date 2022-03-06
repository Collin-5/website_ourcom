from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pytz import timezone
from sqlalchemy import null

# Create your models here.
class Post(models.Model):
    title = models.CharField(
        max_length=400,
        help_text=_("Required: max-400"),
        verbose_name=_("title")
    )

    text = models.TextField(_("text"))
    image = models.ImageField(
        _("image"),
        blank=True,
        upload_to='uploads/',
        help_text=_("can be empty")
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': str(self.pk)})


class Comment(models.Model):
    post = models.ForeignKey(Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    comment = models.TextField(max_length=1000)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.comment[:30]

    class Meta:
        ordering = ['created_at']

    def get_absolute_url(self):
        return reverse('posts')
