# Generated by Django 4.2 on 2023-05-04 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resources',
            name='addr',
            field=models.CharField(help_text='e.g. 0.0.0.0', max_length=15, verbose_name='IP address'),
        ),
    ]
