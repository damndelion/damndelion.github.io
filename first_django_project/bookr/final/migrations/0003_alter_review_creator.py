# Generated by Django 4.1.7 on 2023-03-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0002_book_contributor_review_bookcontributor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='creator',
            field=models.TextField(help_text='Author of rating'),
        ),
    ]
