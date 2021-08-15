# Generated by Django 3.2.5 on 2021-08-15 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210815_1251'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=120)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(max_length=120)),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_items',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.DeleteModel(
            name='BillingAddress',
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]