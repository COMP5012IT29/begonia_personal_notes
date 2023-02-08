# Generated by Django 4.1 on 2023-02-05 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notes", "0002_delete_note"),
    ]

    operations = [
        migrations.CreateModel(
            name="Note",
            fields=[
                ("note_id", models.AutoField(primary_key=True, serialize=False)),
                ("note_title", models.CharField(max_length=100)),
                ("note_content", models.CharField(max_length=3000)),
                ("note_salt", models.CharField(max_length=100)),
                ("note_date", models.DateField()),
                (
                    "n_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "note",},
        ),
    ]