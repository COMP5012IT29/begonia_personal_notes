
from django.urls import path

from user.views import add_user, login_user

urlpatterns = [
    path('signup/', add_user, name="signup"),
    path('login/', login_user, name="login"),
]