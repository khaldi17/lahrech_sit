# Generated by Django 4.2.11 on 2024-10-18 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lahrech_app', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/'),
        ),
    ]
