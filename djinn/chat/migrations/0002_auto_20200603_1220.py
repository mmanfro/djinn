# Generated by Django 3.0.6 on 2020-06-03 15:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='password',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='token',
            field=models.CharField(default=django.utils.timezone.now, editable=False, max_length=255, verbose_name='token'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='content',
            field=models.CharField(max_length=255, verbose_name='content'),
        ),
    ]
