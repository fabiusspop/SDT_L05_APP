# Generated by Django 5.1.4 on 2024-12-07 14:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=20)),
                ('course_id', models.CharField(max_length=20)),
                ('professor_id', models.CharField(max_length=20)),
                ('grade_value', models.DecimalField(decimal_places=2, max_digits=4)),
                ('grade_letter', models.CharField(choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'), ('D+', 'D+'), ('D', 'D'), ('D-', 'D-'), ('F', 'F')], max_length=2)),
                ('semester', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted'), ('APPROVED', 'Approved'), ('DISPUTED', 'Disputed')], default='DRAFT', max_length=20)),
            ],
            options={
                'unique_together': {('student_id', 'course_id', 'semester', 'year')},
            },
        ),
        migrations.CreateModel(
            name='GradeDispute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('submitted_by', models.CharField(max_length=20)),
                ('submitted_date', models.DateTimeField(auto_now_add=True)),
                ('resolution', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('UNDER_REVIEW', 'Under Review'), ('RESOLVED', 'Resolved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20)),
                ('resolved_date', models.DateTimeField(blank=True, null=True)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disputes', to='grading_service.grade')),
            ],
        ),
    ]