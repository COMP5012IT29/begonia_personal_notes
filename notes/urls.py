
from django.urls import path

from notes.views import *

urlpatterns = [
    path('upload/', add_note, name="upload"),
    path('viewNote/', view_note, name="view note"),
    path('editNote/',edit_note,name="update note"),
    path('showNoteList/',show_notes,name='show note list'),
    path('showHint/',view_hint,name='show note password hint'),
    path('search/',search_note,name='search note'),
    path('starNote/',star_note,name="star note"),
    path('recycle/',recycle_note,name="recycle note"),
    path('deleteNote/',delete_note,name="delete note"),
    path('recoverNote/',recovery_note,name="recover note")
]