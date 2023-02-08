from django.urls import path, include
import user

urlpatterns = [
    path('api/', include(('user.urls', 'user'), namespace='user')),
    path('api/', include(('notes.urls', 'notes'), namespace='notes'))
    # other URL patterns ...
]