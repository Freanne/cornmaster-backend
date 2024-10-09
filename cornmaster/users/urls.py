from django.urls import path
from .views import InscriptionView, LoginView

urlpatterns = [
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('login/', LoginView.as_view(), name='login'),
]
