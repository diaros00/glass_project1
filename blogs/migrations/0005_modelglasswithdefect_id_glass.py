# Generated by Django 3.1 on 2021-06-07 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20210607_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelglasswithdefect',
            name='id_glass',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
