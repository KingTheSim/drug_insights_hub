# Generated by Django 5.0.3 on 2024-03-25 13:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proprietary_name', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('international_non_proprietary_name', models.CharField(max_length=30)),
                ('drug_type', models.CharField(blank=True, choices=[('Therapeutic', 'Therapeutic'), ('Experimental', 'Experimental'), ('Preventive', 'Preventive'), ('Diagnostic', 'Diagnostic'), ('Palliative', 'Palliative'), ('Combination', 'Combination'), ('Over-the-Counter (OTC)', 'Over-the-Counter (OTC)'), ('Generic', 'Generic'), ('Biological', 'Biological'), ('Orphan', 'Orphan'), ('Herbal/Alternative', 'Herbal/Alternative'), ('Radiopharmaceutical', 'Radiopharmaceutical')], max_length=30, null=True)),
                ('development_status', models.CharField(choices=[('Preclinical', 'Preclinical'), ('Phase I', 'Phase I'), ('Phase II', 'Phase II'), ('Phase III', 'Phase III'), ('Approved', 'Approved')], default='Preclinical', max_length=30)),
                ('description', models.TextField()),
                ('affiliated_institution', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.affiliation')),
            ],
        ),
        migrations.CreateModel(
            name='ClinicalTrial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
                ('phase', models.CharField(choices=[('Preclinical', 'Preclinical'), ('Phase I', 'Phase I'), ('Phase II', 'Phase II'), ('Phase III', 'Phase III'), ('Approved', 'Approved')], max_length=30)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('affiliation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.affiliation')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='research.drug')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
                ('publication_date', models.DateField(auto_now_add=True)),
                ('modification_date', models.DateField(auto_now=True)),
                ('journal', models.CharField(max_length=30)),
                ('affiliation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.affiliation')),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('trials', models.ManyToManyField(to='research.clinicaltrial')),
            ],
        ),
    ]
