# Generated by Django 3.2.5 on 2021-08-15 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_image_caption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='created_date',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created_date',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='created_date',
            new_name='timestamp',
        ),
    ]
