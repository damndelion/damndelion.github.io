# Generated by Django 4.1.7 on 2023-05-13 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0017_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='avatar',
            field=models.ImageField(default='ava/profile-icon-design-free-vector_1.png', upload_to='ava/'),
        ),
    ]
