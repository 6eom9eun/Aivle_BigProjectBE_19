# Generated by Django 5.0 on 2023-12-22 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0003_quiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='is_correct',
        ),
    ]
