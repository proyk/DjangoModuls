# Generated by Django 4.0.4 on 2022-06-21 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translationPage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]