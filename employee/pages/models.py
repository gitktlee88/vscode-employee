from django.db import models
from django.conf import settings
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse
#
# from django.urls import reverse
# from django.utils.text import slugify
# from django.db.models.signals import post_delete, pre_save
# from django.dispatch import receiver
#
# def upload_location(instance, filename, **kwargs):
#     file_path = 'blog/{author_id}/{title}-{filename}'.format(
#         author_id=str(instance.author.id), title=str(instance.title), filename=filename
#     )
#     return file_path

class BlogPost(models.Model):
    # pk aka id --> numbers
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=120, null=True, blank=True)
    content     = models.TextField(max_length=120, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    # body        = models.TextField(max_length=5000, null=False, blank=False)
    # image       = models.ImageField(upload_to=upload_location, null=False, blank=False)
    # date_published = models.DateTimeField(auto_now_add=True, verbose_name="date_published")
    # date_updated = models.DateTimeField(auto_now=True, verbose_name="date_updated")
    # author_id   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # slugify     = models.SlugField(blank=True, unique=True)

    def __str__(self):
        # return self.test_insert_select_db
        return str(self.user.username)

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self):
        return reverse("api-pages:pages-rud",
        kwargs={'pk': self.pk})    # 'api-pages/1'

    def get_api_url(self, request=None):
        return api_reverse(
            "api-pages:pages-rud",
            kwargs={'pk': self.pk},
            request=request
            )


# @receiver(post_delete, sender=BlogPost)
# def submission_delete(sender, instance, **kwargs):
#     instance.image.delete(False)
#
# def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.author.username + "-" + instance.title)
#
#     pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
