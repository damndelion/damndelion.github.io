# Generated by Django 4.2 on 2023-05-14 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0020_alter_home_map_res'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='about_img',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='home',
            name='img_res',
            field=models.CharField(max_length=1000),
        ),
    ]
