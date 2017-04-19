from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mistune import markdown
from tag.models import Tag


class Article(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    background = models.CharField(null=True, max_length=500)
    raw_content = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    vote = models.IntegerField(default=0)
    pub_date = models.DateTimeField(editable=False)

    @property
    def render_content(self):
        return markdown(self.raw_content)

    @property
    def pub_date_format(self):
        return self.pub_date.strftime('%B %d,%Y')

    def save(self, *args, **kwargs):
        if not self.pub_date:
            self.pub_date = timezone.now()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)
