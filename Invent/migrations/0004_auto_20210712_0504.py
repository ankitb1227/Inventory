# Generated by Django 3.2.5 on 2021-07-12 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invent', '0003_auto_20210711_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='static/uploads'),
        ),
        migrations.AlterField(
            model_name='items',
            name='itemName',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
