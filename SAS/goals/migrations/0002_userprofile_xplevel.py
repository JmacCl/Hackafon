# Generated by Django 3.1.6 on 2021-02-06 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='xpLevel',
            field=models.IntegerField(default=1),
        ),
    ]