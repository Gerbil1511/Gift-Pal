# Generated by Django 5.1.5 on 2025-02-24 19:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wishlistitem',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='wishlistitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='item_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='link',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='thumbnail_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='WishlistCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('occasion_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Wishlist Categories',
                'ordering': ['-occasion_date'],
            },
        ),
        migrations.AddField(
            model_name='wishlistitem',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wishlist.wishlistcategory'),
        ),
    ]
