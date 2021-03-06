# Generated by Django 3.0.5 on 2020-07-14 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_marriage'),
    ]

    operations = [
        migrations.AddField(
            model_name='marriage',
            name='Age',
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='marriage',
            name='Gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='marriage',
            name='Height',
            field=models.FloatField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='marriage',
            name='Mother_tongue',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='marriage',
            name='Sub_cast',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
