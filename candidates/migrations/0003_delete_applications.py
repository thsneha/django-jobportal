# Generated by Django 4.0.4 on 2022-06-19 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0002_applications'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Applications',
        ),
    ]