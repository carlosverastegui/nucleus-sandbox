# Generated by Django 2.2.8 on 2019-12-24 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAPIKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('did', models.CharField(max_length=64)),
                ('api_key', models.CharField(max_length=64)),
            ],
        ),
    ]