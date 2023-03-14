from django.urls import path
from users.views import  UserView, SingleUserView, LoginAPIView

urlpatterns = [
    path('', UserView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('<str:username>', SingleUserView.as_view())
]
