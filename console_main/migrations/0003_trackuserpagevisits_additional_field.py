# Generated by Django 2.2.10 on 2020-04-15 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console_main', '0002_trackuserpagevisits_activity_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackuserpagevisits',
            name='additional_field',
            field=models.CharField(default='', max_length=200),
        ),
    ]
