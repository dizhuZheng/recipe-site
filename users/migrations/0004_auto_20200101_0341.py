# Generated by Django 3.0.1 on 2020-01-01 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191231_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=200, verbose_name='Username'),
        ),
    ]
