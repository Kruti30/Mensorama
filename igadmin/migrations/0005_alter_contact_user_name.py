# Generated by Django 4.1 on 2023-03-27 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igadmin', '0004_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='user_name',
            field=models.CharField(max_length=40),
        ),
    ]
