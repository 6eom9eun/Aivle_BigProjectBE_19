# Generated by Django 5.0 on 2023-12-27 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0006_quiz_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='answer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
