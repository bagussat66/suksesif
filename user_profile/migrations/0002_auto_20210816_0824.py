# Generated by Django 3.2.5 on 2021-08-16 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_profile.district')),
            ],
        ),
        migrations.CreateModel(
            name='Regency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_profile.province')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='regency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_profile.regency'),
        ),
    ]
