from django.urls import path
from .views import home, dashboard, signIn, signUp

urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('signin', signIn, name='signin'),
    path('signup', signUp, name='signup'),
]