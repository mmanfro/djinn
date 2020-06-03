# Generated by Django 3.0.6 on 2020-06-03 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inc_mgmt', '0003_auto_20200527_1239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketupdate',
            old_name='posted_time',
            new_name='time_posted',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(max_length=500, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='ticketupdate',
            name='comment',
            field=models.TextField(max_length=500, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=30, verbose_name='name'),
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('content', models.TextField(verbose_name='content')),
                ('allowed_to_email', models.CharField(max_length=255, null=True, verbose_name='allowed emails')),
                ('time_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='creation time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
