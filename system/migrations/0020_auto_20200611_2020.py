# Generated by Django 3.0.6 on 2020-06-11 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0019_auto_20200611_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventgoer',
            name='chatName',
            field=models.CharField(blank=True, default='NoneYet', max_length=120, null=True),
        ),
    ]