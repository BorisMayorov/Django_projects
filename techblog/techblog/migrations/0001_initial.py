# Generated by Django 3.0.4 on 2020-10-22 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import froala_editor.fields
import techblog.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True, verbose_name='Category Url')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, verbose_name='Tag Url')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Post Url')),
                ('content', froala_editor.fields.FroalaField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to=techblog.models.get_file_path, verbose_name='Select picture')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Published')),
                ('author', models.CharField(blank=True, max_length=100)),
                ('views', models.IntegerField(default=0, verbose_name='Views')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Category', to='techblog.Category')),
                ('tags', models.ManyToManyField(blank=True, related_name='Tags', to='techblog.Tag')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', froala_editor.fields.FroalaField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='techblog.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
            },
        ),
    ]
