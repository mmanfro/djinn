# Generated by Django 3.0.6 on 2020-06-03 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_chatroom_allowed_to_emails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='token',
            field=models.CharField(editable=False, max_length=64, unique=True, verbose_name='token'),
        ),
    ]