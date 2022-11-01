from django.urls import path
from user.views import UserLogin, UserTest, UserLogout, UserView, SingleUserView

urlpatterns = [
    path('', UserView.as_view()),
    path('login',UserLogin.as_view()),
    path('logout', UserLogout.as_view()),
    path('test', UserTest.as_view()),
    # path('<str:username>', SingleUserView.as_view())
]
