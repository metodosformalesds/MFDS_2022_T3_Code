# Generated by Django 4.1.3 on 2022-11-21 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursesapp', '0015_alter_job_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perfil',
            old_name='bio',
            new_name='pais',
        ),
        migrations.RenameField(
            model_name='perfil',
            old_name='usuario',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='web',
        ),
        migrations.AddField(
            model_name='perfil',
            name='avatar',
            field=models.ImageField(default='default', null=True, upload_to='profile_images'),
        ),
        migrations.AddField(
            model_name='perfil',
            name='skills',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
