from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

# Create your tests here.


class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_url(self):
        url = reverse("home")
        self.assertEqual(url, "/")

    def test_signup_url(self):
        url = reverse("signup")
        self.assertEqual(url, "/signup")

    def test_signin_url(self):
        url = reverse("signin")
        self.assertEqual(url, "/signin")

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEqual(url, "/logout")

    def test_dashboard_url(self):
        url = reverse("dashboard")
        self.assertEqual(url, "/dashboard")

    def test_profits_url(self):
        url = reverse("profits")
        self.assertEqual(url, "/profits")

    def test_spending_url(self):
        url = reverse("spending")
        self.assertEqual(url, "/spending")

    def test_profit_delete_url(self):
        url = reverse("profitDel", kwargs={"id": 1})
        self.assertEqual(url, "/profitDel/1")

    def test_profit_edit_url(self):
        url = reverse("profitEdit", kwargs={"id": 1})
        self.assertEqual(url, "/profitEdit/1")

    def test_spending_delete_url(self):
        url = reverse("spendingDel", kwargs={"id": 1})
        self.assertEqual(url, "/spendingDel/1")

    def test_spending_edit_url(self):
        url = reverse("spendingEdit", kwargs={"id": 1})
        self.assertEqual(url, "/spendingEdit/1")
