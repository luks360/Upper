from django.urls import path
from .views import (
    home,
    dashboard,
    signIn,
    signUp,
    exit,
    profits,
    spending,
    profitDel,
    profitEdit,
    spendingDel,
    spendingEdit,
)

urlpatterns = [
    path("", home, name="home"),
    path("dashboard", dashboard, name="dashboard"),
    path("signin", signIn, name="signin"),
    path("signup", signUp, name="signup"),
    path("logout", exit, name="logout"),
    # path('profile', profile, name='profile'),
    path("profits", profits, name="profits"),
    path("spending", spending, name="spending"),
    path("profitDel/<int:id>", profitDel, name="profitDel"),
    path("profitEdit/<int:id>", profitEdit, name="profitEdit"),
    path("spendingDel/<int:id>", spendingDel, name="spendingDel"),
    path("spendingEdit/<int:id>", spendingEdit, name="spendingEdit"),
]
