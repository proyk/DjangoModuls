# Generated by Django 4.0.4 on 2022-05-27 08:44

from django.db import migrations, models
import django.db.models.deletion
import languages.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('languages', '0001_initial'),
        ('attribute', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeTranslate',
            fields=[
                ('attributeTranslateId', models.AutoField(primary_key=True, serialize=False)),
                ('fieldLabel', models.CharField(max_length=15, verbose_name='Label')),
                ('fieldId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attribute.attributefields')),
                ('languageId', models.ForeignKey(default=languages.models.get_language, on_delete=django.db.models.deletion.CASCADE, to='languages.language')),
            ],
        ),
    ]