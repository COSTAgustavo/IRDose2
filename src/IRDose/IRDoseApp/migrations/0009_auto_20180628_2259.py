# Generated by Django 2.0.4 on 2018-06-28 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IRDoseApp', '0008_auto_20180628_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cumactivity',
            name='CT_Organ',
            field=models.FileField(blank=True, null=True, upload_to='../media/<django.db.models.fields.CharField><django.db.models.fields.CharField>', verbose_name='Source/target Organ'),
        ),
    ]
