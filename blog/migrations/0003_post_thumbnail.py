# Generated by Django 2.1.3 on 2018-12-08 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20181203_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.FileField(blank=True, null=True, upload_to='blog_thumbnails'),
        ),
    ]
