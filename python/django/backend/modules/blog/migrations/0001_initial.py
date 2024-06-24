# Generated by Django 4.2.11 on 2024-06-20 16:28

import django.core.validators
import django.db.models.deletion
import mptt.fields
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название категории')),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='URL категории')),
                ('description', models.TextField(max_length=300, verbose_name='Описание категории')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent',
                 mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='children', to='blog.category',
                                            verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'app_categories',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL')),
                ('short_description', models.TextField(max_length=500, verbose_name='Краткое описание')),
                ('full_description', models.TextField(verbose_name='Полное описание')),
                ('thumbnail', models.ImageField(blank=True, upload_to='images/thumbnails/%Y/%m/%d/', validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))], verbose_name='Превью поста')),
                ('status',
                 models.CharField(choices=[('published', 'Опубликовано'), ('draft', 'Черновик')], default='published',
                                  max_length=10, verbose_name='Статус поста')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('fixed', models.BooleanField(default=False, verbose_name='Зафиксировано')),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT,
                                             related_name='author_posts', to=settings.AUTH_USER_MODEL,
                                             verbose_name='Автор')),
                ('category',
                 mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='articles',
                                            to='blog.category', verbose_name='Категория')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.',
                                                         through='taggit.TaggedItem', to='taggit.Tag',
                                                         verbose_name='Tags')),
                ('updater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                              related_name='updater_posts', to=settings.AUTH_USER_MODEL,
                                              verbose_name='Обновил')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'db_table': 'app_articles',
                'ordering': ['-fixed', '-time_create'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=3000, verbose_name='Текст комментария')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('status',
                 models.CharField(choices=[('published', 'Опубликовано'), ('draft', 'Черновик')], default='published',
                                  max_length=10, verbose_name='Статус поста')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments',
                                              to='blog.article', verbose_name='Статья')),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_author',
                                   to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('parent',
                 mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='children', to='blog.comment',
                                            verbose_name='Родительский комментарий')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'db_table': 'app_comments',
                'ordering': ['-time_create'],
                'indexes': [models.Index(fields=['-time_create', 'time_update', 'status', 'parent'],
                                         name='app_comment_time_cr_0c0ec5_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['-fixed', '-time_create', 'status'], name='app_article_fixed_e300bf_idx'),
        ),
    ]
