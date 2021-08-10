# Generated by Django 3.2.5 on 2021-08-07 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20210807_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_author', models.CharField(max_length=50, verbose_name='Автор комментария')),
                ('comment_text', models.CharField(max_length=200, verbose_name='Текст комментария')),
                ('published', models.DateTimeField(verbose_name='Дата публикации')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-published'],
            },
        ),
    ]