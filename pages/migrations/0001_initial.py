# Generated by Django 4.2 on 2023-04-13 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('ip', models.CharField(max_length=30)),
                ('connected', models.BooleanField()),
            ],
        ),
    ]
