# Generated by Django 5.0 on 2023-12-27 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0010_delete_spelling'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='quiz_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
