# Generated by Django 2.2.11 on 2020-05-02 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200430_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursearrangement',
            name='term',
            field=models.CharField(max_length=20, verbose_name='地点'),
        ),
        migrations.AlterField(
            model_name='coursearrangement',
            name='week_begin',
            field=models.CharField(max_length=20, verbose_name='星期'),
        ),
        migrations.AlterField(
            model_name='coursearrangement',
            name='week_end',
            field=models.CharField(max_length=20, verbose_name='节次'),
        ),
    ]
