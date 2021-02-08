from django import template
from techblog.models import Category, Post, Tag
from django.db.models import Count

register = template.Library()


@register.simple_tag(name='get_cat')
def get_categories():

    return Category.objects.annotate(cnt=Count('Category')).filter(cnt__gt=0)


@register.simple_tag(name='all_posts')
def get_posts():
    return Post.objects.all().select_related('category')


@register.simple_tag(name='popular_posts')
def get_posts():
    return Post.objects.order_by('-hit_count_generic__hits')[:6]


@register.inclusion_tag("techblog/tags_tpl.html")
def get_tags():
    tags = Tag.objects.all()

    return {"tags": tags, }
