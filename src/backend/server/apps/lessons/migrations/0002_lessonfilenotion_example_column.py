# Generated by Django 4.1.3 on 2022-11-28 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lessonfilenotion",
            name="example_column",
            field=models.TextField(null=True),
        ),
    ]
