# Generated by Django 2.2 on 2021-05-03 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0010_remove_book_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='Description',
            field=models.CharField(default='Lorem ipsum dolor, sit amet consectetur adipisicing elit. Error, eos. Praesentium distinctio aut quas consectetur neces    ', max_length=100),
            preserve_default=False,
        ),
    ]