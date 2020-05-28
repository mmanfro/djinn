# Generated by Django 3.0.6 on 2020-05-27 15:39

from django.db import migrations, models
import inc_mgmt.models


class Migration(migrations.Migration):

    dependencies = [
        ('inc_mgmt', '0002_auto_20200526_0235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='knox_id',
            new_name='knoxid',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=inc_mgmt.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='ticketupdate',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=inc_mgmt.models.get_upload_path),
        ),
    ]
