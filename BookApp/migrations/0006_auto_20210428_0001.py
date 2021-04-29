# Generated by Django 2.2 on 2021-04-28 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0005_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='book',
            name='yearPublished',
            field=models.IntegerField(),
        ),
    ]
