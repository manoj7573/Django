# Generated by Django 3.1.3 on 2021-02-04 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20200725_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Hotel',
        ),
    ]
