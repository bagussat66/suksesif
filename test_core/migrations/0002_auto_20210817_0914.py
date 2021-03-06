# Generated by Django 3.2.5 on 2021-08-17 02:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('test_core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testattempt',
            name='expected',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='testattempt',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='testattempt',
            name='type',
            field=models.CharField(blank=True, choices=[('MBTI', 'Myers-Briggs Type Indicator'), ('BFI', 'Big Five Inventory'), ('PAPI', 'PAPI Kostick'), ('EPPS', 'Edward Personal Preference Schedule'), ('DISC', 'Dominant, Influencing, Steadiness, Conscientiousness'), ('MSDT', 'Management Style Diagnostic Test'), ('PF16', 'Personality Factor Sixteen'), ('TPA', 'Tes Potensi Akademik')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='tester',
            name='type',
            field=models.CharField(blank=True, choices=[('MBTI', 'Myers-Briggs Type Indicator'), ('BFI', 'Big Five Inventory'), ('PAPI', 'PAPI Kostick'), ('EPPS', 'Edward Personal Preference Schedule'), ('DISC', 'Dominant, Influencing, Steadiness, Conscientiousness'), ('MSDT', 'Management Style Diagnostic Test'), ('PF16', 'Personality Factor Sixteen'), ('TPA', 'Tes Potensi Akademik')], max_length=30, null=True),
        ),
    ]
