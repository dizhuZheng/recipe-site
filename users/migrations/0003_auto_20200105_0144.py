# Generated by Django 3.0.1 on 2020-01-05 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200105_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='cover',
            field=models.ImageField(upload_to='img/'),
        ),
    ]
