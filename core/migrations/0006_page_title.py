# Generated by Django 3.2.5 on 2021-08-19 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210819_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='title',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]
