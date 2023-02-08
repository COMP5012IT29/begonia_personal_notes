from django.db import models


class Note(models.Model):
    note_id = models.AutoField(primary_key = True)
    note_title = models.CharField(max_length=100, default='new diary')
    note_content = models.BinaryField(null=True)
    note_salt = models.CharField(max_length=100, null=True)
    note_iv = models.BinaryField(null=True)
    note_date = models.DateField(null=True)
    note_tag = models.CharField(max_length=100,null=True)
    note_deleted = models.BooleanField(default=False)
    note_stared = models.BooleanField(default=False)
    note_user = models.ForeignKey('user.User', on_delete=models.CASCADE,null=True)
    note_pwd_hint = models.CharField(max_length=100,null=True)
