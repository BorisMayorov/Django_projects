from django.db import models
from froala_editor.fields import FroalaField
from django.template.defaultfilters import slugify
from datetime import datetime
import uuid
import os
from django.urls import reverse


# Create your models here.


def get_file_path(instance, filename):
    ext = filename.partition('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('pictures', filename)


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Url')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique=True)
    image = models.ImageField(upload_to=get_file_path)
    content = FroalaField(blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Published')
    category = models.ForeignKey(
        Category, null=True, related_name='posts', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)+'-' + \
                slugify(self.created_at.ctime())
        super(Post, self).save()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
