# Generated by Django 3.0.1 on 2019-12-31 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default=0, max_length=20),
            preserve_default=False,
        ),
    ]