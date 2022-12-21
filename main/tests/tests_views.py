import datetime
from django.test import Client, TestCase
from main.models import User, Profits, GroupProfits, Spending, GroupSpending
from django.urls import reverse

# Create your tests here.


class TestViews(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", email="test")
        user.set_password("12345")
        user.save()
        self.clientV = Client()
        self.client.login(username="testuser", password="12345")

        self.group = GroupProfits.objects.create(name="testando", user=user)
        self.profit = Profits.objects.create(
            id=1,
            name="test",
            value=20,
            group=self.group,
            date=datetime.date(2013, 12, 3),
            user=user,
        )

        self.groupS = GroupSpending.objects.create(name="testando", user=user)
        self.spending = Spending.objects.create(
            id=1,
            name="test",
            value=20,
            group=self.groupS,
            date=datetime.date(2013, 12, 3),
            user=user,
        )

    def test_home_url(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        response = self.clientV.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signin_url(self):
        response = self.clientV.get(reverse("signin"))
        self.assertEqual(response.status_code, 200)

    def test_signup_logged_url(self):
        response = self.client.get(reverse("signup"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signin_logged_url(self):
        response = self.client.get(reverse("signin"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get(reverse("logout"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_profits_url(self):
        response = self.client.get(reverse("profits"))
        self.assertEqual(response.status_code, 200)

    def test_spending_url(self):
        response = self.client.get(reverse("spending"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_not_logged_url(self):
        response = self.clientV.get(reverse("dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profits_not_logged_url(self):
        response = self.clientV.get(reverse("profits"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_spending_not_logged_url(self):
        response = self.clientV.get(reverse("spending"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profit_delete_url(self):
        response = self.client.delete(
            reverse("profitDel", kwargs={"id": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_profit_edit_url(self):
        response = self.client.post(
            reverse("profitEdit", kwargs={"id": 1}),
            {
                "name": "name",
                "value": 20,
                "date": datetime.date(2012, 12, 20),
                "group": self.groupS,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_profit_edit_data_none_url(self):
        response = self.client.get(reverse("profitEdit", kwargs={"id": 1}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_spending_delete_url(self):
        response = self.client.delete(
            reverse("spendingDel", kwargs={"id": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_spending_edit_url(self):
        response = self.client.post(
            reverse("spendingEdit", kwargs={"id": 1}),
            {
                "name": "name",
                "value": 20,
                "date": datetime.date(2012, 12, 20),
                "group": self.groupS,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_spending_edit_data_none_url(self):
        response = self.client.get(
            reverse("spendingEdit", kwargs={"id": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_spending_create_url(self):
        response = self.client.post(
            reverse("spending"),
            {
                "name": "name",
                "value": 20,
                "date": datetime.date(2012, 12, 20),
                "group": self.groupS,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_profit_create_url(self):
        response = self.client.post(
            reverse("profits"),
            {
                "name": "name",
                "value": 20,
                "date": datetime.date(2012, 12, 20),
                "group": self.group,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
