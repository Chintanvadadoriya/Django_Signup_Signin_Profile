# Generated by Django 4.0.2 on 2022-03-10 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Date_Of_Birth',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
