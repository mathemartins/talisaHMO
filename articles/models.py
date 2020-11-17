from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.text import slugify
from django.conf import settings

User = settings.AUTH_USER_MODEL


def upload_dir(instance, filename):
    return "{}/{}".format(instance.author, filename)


class ArticleQuerySet(models.query.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().not_draft()


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    image_url = models.ImageField(blank=True, null=True, upload_to=upload_dir)
    description = models.TextField()
    body = models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    draft = models.BooleanField(default=True)
    objects = ArticleManager()

    class Meta:
        verbose_name_plural = "Articles"
        ordering = ("-created",)
        unique_together = ['title', 'slug']

    def __str__(self):
        return self.title

    def check_image_url(self):
        if self.image_url:
            return self.image_url.url
        return "https://talisa-hmo.s3.eu-west-2.amazonaws.com/images/social-media.jpg"

    def get_absolute_url(self):
        return reverse("articles:article_detail", kwargs={"slug": self.slug})

    @property
    def was_published_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)


def article_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        new_slug = "{}-{}".format(instance.title, instance.id)
        try:
            instance.slug = instance.slug
        except Article.DoesNotExist:
            instance.slug = slugify(new_slug)
        except Article.MultipleObjectsReturned:
            instance.slug = slugify(new_slug, instance.slug)
        else:
            pass


pre_save.connect(article_pre_save_signal, sender=Article)


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def approved(self):
        self.approved = True
        self.save()

    def __str__(self):
        return '{} - {}'.format(self.content, self.by)

    # def get_comment_message_as_markdown(self):
    #     return mark_safe(markdown(self.content, safe_mode='escape'))


    class Meta:
        ordering = ['created_on']


class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    replied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['replied_on']
