# Generated by Django 4.1.3 on 2022-11-23 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coursesapp", "0019_skills"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="category",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
