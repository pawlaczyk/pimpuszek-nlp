# Generated by Django 4.1.3 on 2022-12-03 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0003_alter_lessonquiznotion_notion_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lessonquiznotion",
            name="filepath",
            field=models.CharField(max_length=255),
        ),
    ]