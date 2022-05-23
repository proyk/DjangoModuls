# Generated by Django 4.0.4 on 2022-05-23 06:35

from django.db import migrations, models
import django.db.models.deletion
import languages.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('languages', '0001_initial'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='content',
            fields=[
                ('contentId', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', tinymce.models.HTMLField()),
                ('language', models.ForeignKey(default=languages.models.get_language, on_delete=django.db.models.deletion.CASCADE, to='languages.language')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.page')),
            ],
        ),
    ]
