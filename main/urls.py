from django.urls import path

from .views import (dashboard, exit, home, profitDel, profitEdit, profits,
                    signIn, signUp, spending, spendingDel, spendingEdit)

urlpatterns = [
    path("", home.as_view(), name="home"),
    path("dashboard", dashboard.as_view(), name="dashboard"),
    path("signin", signIn.as_view(), name="signin"),
    path("signup", signUp.as_view(), name="signup"),
    path("logout", exit.as_view(), name="logout"),
    # path('profile', profile, name='profile'),
    path("profits", profits.as_view(), name="profits"),
    path("spending", spending.as_view(), name="spending"),
    path("profitDel/<int:pk>", profitDel.as_view(), name="profitDel"),
    path("profitEdit/<int:pk>", profitEdit.as_view(), name="profitEdit"),
    path("spendingDel/<int:pk>", spendingDel.as_view(), name="spendingDel"),
    path("spendingEdit/<int:pk>", spendingEdit.as_view(), name="spendingEdit"),
]
