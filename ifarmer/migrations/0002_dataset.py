# Generated by Django 4.2.9 on 2024-04-27 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifarmer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='datasets/')),
            ],
        ),
    ]
