from django.urls import path
from user.views import UserLogin, UserRegister, UserTest, UserLogout, UserList

urlpatterns = [
    path('login',UserLogin.as_view()),
    path('register', UserRegister.as_view()),
    path('logout', UserLogout.as_view()),
    path('test', UserTest.as_view()),
    path('list', UserList.as_view())
]
