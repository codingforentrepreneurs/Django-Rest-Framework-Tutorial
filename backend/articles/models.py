from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL # auth.User


class ArticleManager(models.Manager):
    def public(self):
        now = timezone.now()
        return self.get_queryset().filter(make_public=True, publish_date__lte=now)

class Article(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    body = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True, help_text='Use commas to separate tags')
    make_public = models.BooleanField(default=False, null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    objects = ArticleManager()

    def get_absolute_url(self):
        return f"/api/articles/{self.pk}/"

    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def path(self):
        return f"/articles/{self.pk}/"

    def is_public(self):
        if self.publish_date is None:
            return False
        if self.make_public is None:
            return False
        now = timezone.now()
        is_in_past = now >= self.publish_date
        return is_in_past and self.make_public

    def get_tags_list(self):
        if not self.tags:
            return []
        return [x.lower().strip() for x in self.tags.split(',')]

    def save(self, *args, **kwargs):
        if self.tags:
            if self.tags.endswith(","):
                self.tags = self.tags[:-1]
            if self.tags.startswith(","):
                self.tags = self.tags[1:]
            self.tags = f"{self.tags}".lower()
        if self.make_public and self.publish_date is None:
            self.publish_date = timezone.now()
        super().save(*args, **kwargs)
