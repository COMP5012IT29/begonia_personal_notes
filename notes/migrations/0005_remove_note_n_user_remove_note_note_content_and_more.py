# Generated by Django 4.1 on 2023-02-05 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0004_alter_note_table"),
    ]

    operations = [
        migrations.RemoveField(model_name="note", name="n_user",),
        migrations.RemoveField(model_name="note", name="note_content",),
        migrations.RemoveField(model_name="note", name="note_date",),
        migrations.RemoveField(model_name="note", name="note_salt",),
        migrations.RemoveField(model_name="note", name="note_title",),
    ]
