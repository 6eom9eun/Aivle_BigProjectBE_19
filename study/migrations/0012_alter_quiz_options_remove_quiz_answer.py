# Generated by Django 5.0 on 2023-12-28 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0011_quiz_quiz_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['-quiz_id']},
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='answer',
        ),
    ]
