# Generated by Django 4.1.3 on 2022-11-13 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coursesapp", "0005_courses_delete_curso"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courses",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="courses",
            name="rating",
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]