# Generated by Django 2.0.4 on 2018-06-28 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IRDoseApp', '0006_auto_20180628_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cumactivity',
            name='CT_Organ',
            field=models.FileField(blank=True, null=True, upload_to='../data/', verbose_name='Source/target Organ'),
        ),
        migrations.AlterField(
            model_name='cumactivity',
            name='CT_Target_1',
            field=models.FileField(blank=True, null=True, upload_to='../data/', verbose_name='Second Target Organ'),
        ),
        migrations.AlterField(
            model_name='cumactivity',
            name='CT_Target_2',
            field=models.FileField(blank=True, null=True, upload_to='../data/', verbose_name='Third Target Organ'),
        ),
    ]
