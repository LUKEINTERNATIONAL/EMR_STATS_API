from django.urls import path
from users.views import  UserView, SingleUserView, LoginAPIView,HisOfficer

urlpatterns = [
    path('', UserView.as_view()),
    path('his_officer', HisOfficer.as_view()),
    path('<int:pk>', UserView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('<str:username>', SingleUserView.as_view())
]
