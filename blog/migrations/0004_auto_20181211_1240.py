# Generated by Django 2.1.3 on 2018-12-11 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_thumbnail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': (('view_original_img', 'Can view the original image of a blog post'),)},
        ),
    ]
