# Generated by Django 3.2.5 on 2021-07-20 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='seen_posts',
            field=models.ManyToManyField(blank=True, to='Blog.Post'),
        ),
    ]
