# Generated by Django 3.2.8 on 2022-02-17 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0004_auto_20220218_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='username',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
