# Generated by Django 3.0.6 on 2020-05-22 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=50, unique=True)),
                ('birth', models.DateField(null=True)),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('alarm_confirm', models.BooleanField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
