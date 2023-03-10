
from django.urls import path

from user.views import add_user, login_user, update_user, delete_user
urlpatterns = [
    path('signup/', add_user, name="signup"),
    path('login/', login_user, name="login"),
    path('UpdateUserInfo/', update_user, name="UpdateUserInfo"),
    path('delete/', delete_user, name="delete_account"),
]