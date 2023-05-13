# Generated by Django 4.1.7 on 2023-05-13 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0012_menu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='ava/')),
                ('username', models.CharField(default="{% static 'images/profile.png' %}", max_length=70)),
            ],
        ),
    ]
