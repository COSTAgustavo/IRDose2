# Generated by Django 2.0.4 on 2018-06-27 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IRDoseApp', '0003_auto_20180625_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='cumactivity',
            name='CT_Target_1',
            field=models.FileField(blank=True, null=True, upload_to='../media/', verbose_name='Second Target Organ'),
        ),
        migrations.AddField(
            model_name='cumactivity',
            name='CT_Target_2',
            field=models.FileField(blank=True, null=True, upload_to='../media/', verbose_name='Third Target Organ'),
        ),
        migrations.AlterField(
            model_name='cumactivity',
            name='CT_Organ',
            field=models.FileField(blank=True, null=True, upload_to='../media/', verbose_name='Source/target Organ'),
        ),
        migrations.AlterField(
            model_name='cumactivity',
            name='CT_Patient',
            field=models.FileField(blank=True, null=True, upload_to='../media/', verbose_name='Patient CT'),
        ),
    ]