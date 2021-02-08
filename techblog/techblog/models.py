from django.db import models
from froala_editor.fields import FroalaField
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.contrib.auth.models import User

import uuid
import os

# Create your models here.


def get_file_path(instance, filename):
    ext = filename.partition('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('pictures', filename)


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Category Url')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("get_category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['pk']


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Tag Url')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("get_tag", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']


class Post(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True,
                            verbose_name='Post Url')
    content = FroalaField(blank=True)

    picture = models.ImageField(
        upload_to=get_file_path, blank=True, verbose_name='Select picture')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='Category')
    tags = models.ManyToManyField(Tag, blank=True, related_name='Tags')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Published')
    author = models.CharField(max_length=100, blank=True)
    views = models.IntegerField(default=0, verbose_name='Views')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk')
    related_query_name = 'hit_count_generic_relation'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("get_post", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_comments')
    body = FroalaField(plugins=('emoticons', 'char_counter',
                                ), max_length=500, verbose_name='Comment')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-updated', '-created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.post)
