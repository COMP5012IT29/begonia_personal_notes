# Generated by Django 4.1 on 2023-02-05 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0007_note_note_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="note", name="note_iv", field=models.BinaryField(null=True),
        ),
    ]
