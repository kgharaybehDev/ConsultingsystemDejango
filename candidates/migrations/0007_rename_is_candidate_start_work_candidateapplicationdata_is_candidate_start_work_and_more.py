# Generated by Django 5.1.3 on 2024-11-26 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "candidates",
            "0006_rename_is_candidate_start_work_candidateapplicationdata_is_candidate_start_work_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="candidateapplicationdata",
            old_name="is_candidate_Start_Work",
            new_name="is_candidate_start_work",
        ),
        migrations.RenameField(
            model_name="historicalcandidateapplicationdata",
            old_name="is_candidate_Start_Work",
            new_name="is_candidate_start_work",
        ),
    ]
