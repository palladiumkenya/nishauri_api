# Generated by Django 3.0.6 on 2020-06-18 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0011_auto_20200603_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependants',
            name='first_name',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='dependants',
            name='surname',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default='2020-06-06'),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(default='2020-06-06'),
        ),
    ]
