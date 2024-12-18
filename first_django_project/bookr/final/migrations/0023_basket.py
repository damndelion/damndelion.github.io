# Generated by Django 5.1.1 on 2024-11-06 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0022_alter_home_about_res'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(help_text='Username', max_length=40)),
                ('items', models.JSONField(default=dict)),
            ],
        ),
    ]