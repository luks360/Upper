from django.urls import path
from .views import home, dashboard, signIn, signUp, exit

urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('signin', signIn, name='signin'),
    path('signup', signUp, name='signup'),
    path('logout', exit, name='logout')
]