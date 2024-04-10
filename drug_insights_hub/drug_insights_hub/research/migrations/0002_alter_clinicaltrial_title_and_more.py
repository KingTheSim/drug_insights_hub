# Generated by Django 5.0.3 on 2024-04-08 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicaltrial',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='international_non_proprietary_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]