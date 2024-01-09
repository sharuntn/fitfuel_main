# Generated by Django 4.2.3 on 2024-01-04 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='abdomen',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bmi',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
