# Generated by Django 4.1.3 on 2022-11-13 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coursesapp", "0002_course"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="instructor",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="course",
            name="platform",
            field=models.CharField(max_length=20, null=True),
        ),
    ]
