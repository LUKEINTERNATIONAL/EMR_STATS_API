from django.urls import path
from users.views import  UserView, SingleUserView

urlpatterns = [
    path('', UserView.as_view()),
    path('<str:username>', SingleUserView.as_view())
]
