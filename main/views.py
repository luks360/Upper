from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.edit import DeleteView

from main.forms import (EditProfitsForm, EditSpendingForm,
                        RegisterGroupProfitsForm, RegisterGroupSpendingForm,
                        RegisterProfitsForm, RegisterSpendingForm,
                        RegisterUserForm)
from main.models import GroupProfits, GroupSpending, Profits, Spending, User

# Create your views here.


class home(View):
    def get(self, request):

        return render(request, "main/index.html")


class dashboard(View, LoginRequiredMixin):
    
    login_url = "/signin"

    currentDateTime = datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    month = date.strftime("%m")

    def get(self, request):

        mes_profits = (
            Profits.objects.filter(user=request.user, date__year=self.year)
            .dates("date", "year")
            .values("date")
            .annotate(Sum("value"))
        )

        mes_spending = (
            Spending.objects.filter(user=request.user, date__year=self.year)
            .dates("date", "year")
            .values("date")
            .annotate(Sum("value"))
        )

        labels = []
        values = []
        values1 = []
        colorP = "success"
        colorS = "success"
        colorG = "success"

        for data in range(len(mes_profits)):  # pragma: no cover
            labels.append(mes_profits[data]["date"].strftime("%B"))
            values.append(float(mes_profits[data]["value__sum"]))

        for data in range(len(mes_spending)):  # pragma: no cover
            values1.append(float(mes_spending[data]["value__sum"]))

        profitsT = 0
        p = Profits.objects.filter(user=request.user, date__month=self.month, date__year=self.year)
        for item in p:  # pragma: no cover
            profitsT += item.value

        spendingT = 0
        s = Spending.objects.filter(user=request.user, date__month=self.month, date__year=self.year)
        for item in s:  # pragma: no cover
            spendingT += item.value

        profitsTA = 0
        pa = Profits.objects.filter(
            user=request.user, date__month=self.date.month - 1, date__year=self.year
        )
        for item in pa:  # pragma: no cover
            profitsTA += item.value

        spendingTA = 0
        sa = Spending.objects.filter(
            user=request.user, date__month=self.date.month - 1, date__year=self.year
        )
        for item in sa:  # pragma: no cover
            spendingTA += item.value

        if profitsT or profitsTA:  # pragma: no cover
            perP = ((profitsT - profitsTA) / profitsT) * 100
        else:
            perP = 0

        if spendingT or spendingTA:  # pragma: no cover
            perS = ((spendingT - spendingTA) / spendingT) * 100
        else:
            perS = 0

        gainA = profitsTA - spendingTA

        gain = profitsT - spendingT

        if gain == None or gainA == None:  # pragma: no cover
            perG = ((gain - gainA) / gain) * 100
        else:
            perG = 0

        if perP < 0:  # pragma: no cover
            colorP = "danger"
        elif perP == 0:
            colorP = "secondary"

        if perS < 0:  # pragma: no cover
            colorS = "danger"
        elif perS == 0:
            colorS = "secondary"

        if perG < 0:  # pragma: no cover
            colorG = "danger"
        elif perG == 0:  # pragma: no cover
            colorG = "secondary"

        item = {
            "date": labels,
            "value": values,
            "value1": values1,
            "totais": {
                "profitsT": profitsT,
                "spendingT": spendingT,
                "gain": gain,
                "perP": perP,
                "perS": perS,
                "perG": perG,
                "colorP": colorP,
                "colorS": colorS,
                "colorG": colorG,
            },
        }

        return render(request, "dashboard/dashboard.html", item)


# def profile(request):
#     if request.user.is_authenticated == False:
#         return redirect('signin')

#     return render(request, 'dashboard/profile.html')


class profits(View, LoginRequiredMixin):

    login_url = "/signin"

    currentDateTime = datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    month = date.strftime("%m")

    def post(self, request):

        result = (
            Profits.objects.values("group")
            .filter(user=request.user, date__year=self.year, date__month=self.month)
            .annotate(Sum("value"))
        )

        gr1 = GroupProfits.objects.filter(user=request.user)

        gr = []
        for i in range(len(result)):  # pragma: no cover
            if result:
                gr.append(
                    {
                        "group": gr1[i].name,
                        "value": result[i]["value__sum"],
                    }
                )
            else:
                gr.append(
                    {
                        "group": gr1[i].name,
                        "value": 0,
                    }
                )
        profits = Profits.objects.filter(user=request.user).order_by("-id")
        paginator = Paginator(profits, 6)
        page = request.GET.get("page")
        profitsR = paginator.get_page(page)
        group_profits_form = RegisterGroupProfitsForm(data=request.POST)
        profits_form = RegisterProfitsForm(request.POST, user=request.user)

        if profits_form:  # pragma: no cover
            if profits_form.is_valid():
                form = profits_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("profits")

        if group_profits_form:  # pragma: no cover
            try:
                group_aux = GroupProfits.objects.get(name=request.POST["name"])
                form = RegisterGroupProfitsForm()
                formE = EditProfitsForm(user=request.user)
                form1 = RegisterProfitsForm(user=request.user)
                item = {
                    "form": form,
                    "form1": form1,
                    "formE": formE,
                    "groups": gr,
                    "profits": profitsR,
                    "msg": "Erro! Já existe um grupo com o mesmo nome",
                }

                if group_aux:  # pragma: no cover
                    return render(request, "dashboard/profits.html", item)

            except GroupProfits.DoesNotExist:
                if group_profits_form.is_valid():
                    form = group_profits_form.save(commit=False)
                    form.user = request.user
                    form.save()
                    return render(request, "dashboard/profits.html", item)

    def get(self, request):
        result = (
            Profits.objects.values("group")
            .filter(user=request.user, date__year=self.year, date__month=self.month)
            .annotate(Sum("value"))
        )

        gr1 = GroupProfits.objects.filter(user=request.user)

        gr = []
        for i in range(len(result)):  # pragma: no cover
            if result:
                gr.append(
                    {
                        "group": gr1[i].name,
                        "value": result[i]["value__sum"],
                    }
                )
            else:
                gr.append(
                    {
                        "group": gr1[i].name,
                        "value": 0,
                    }
                )
        profits = Profits.objects.filter(user=request.user).order_by("-id")
        paginator = Paginator(profits, 6)
        page = request.GET.get("page")
        profitsR = paginator.get_page(page)
        form1 = RegisterProfitsForm(user=request.user)
        form = RegisterGroupProfitsForm()
        formE = EditProfitsForm(user=request.user)
        valorR = 0
        p = Profits.objects.filter(
            user=request.user, date__year=self.year, date__month=self.month
        )
        for item in p:  # pragma: no cover
            valorR += item.value

        item = {
            "form1": form1,
            "profits": profitsR,
            "form": form,
            "formE": formE,
            "groups": gr,
            "result": valorR,
        }

        return render(request, "dashboard/profits.html", item)


class profitDel(DeleteView, LoginRequiredMixin):
    model = Profits
    success_url = "/profits"
    login_url = "/signin"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class profitEdit(View, LoginRequiredMixin):

    login_url = "/signin"

    def post(self, request, *args, **kwargs):

        profit = get_object_or_404(Profits, pk=kwargs.get("pk"))
        form = EditProfitsForm(request.POST, instance=profit, user=request.user)

        if form.is_valid():  # pragma: no cover
            profit = form.save(commit=False)
            profit.name = form.cleaned_data["name"]
            profit.value = form.cleaned_data["value"]
            profit.group = form.cleaned_data["group"]
            profit.date = form.cleaned_data["date"]
            profit.save()
            return redirect("profits")
        else:
            form = EditProfitsForm(instance=profit, user=request.user)
            return redirect("profits")


class spending(View, LoginRequiredMixin):

    login_url = "/signin"

    currentDateTime = datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    month = date.strftime("%m")
    item = {}

    def post(self, request):

        result = (
            Spending.objects.values("group")
            .filter(user=request.user, date__year=self.year, date__month=self.month)
            .annotate(Sum("value"))
        )

        gr1 = GroupSpending.objects.filter(user=request.user)

        gr = []
        for i in range(len(result)):  # pragma: no cover
            if result:
                gr.append(
                    {
                        "group": gr1[i].name,
                        "value": result[i]["value__sum"],
                    }
                )
            else:
                gr.append(
                    {
                        "group": gr1[i].name,
                        "value": 0,
                    }
                )
        spending = Spending.objects.filter(user=request.user).order_by("-id")
        paginator = Paginator(spending, 6)
        page = request.GET.get("page")
        spendingR = paginator.get_page(page)
        group_spending_form = RegisterGroupSpendingForm(data=request.POST)
        spending_form = RegisterSpendingForm(request.POST, user=request.user)

        if spending_form:  # pragma: no cover
            if spending_form.is_valid():
                form = spending_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("spending")

        if group_spending_form:  # pragma: no cover
            try:
                group_aux = GroupSpending.objects.get(name=request.POST["name"])
                form = RegisterGroupSpendingForm()
                formE = EditSpendingForm(user=request.user)
                form1 = RegisterSpendingForm(user=request.user)
                self.item = {
                    "form": form,
                    "form1": form1,
                    "formE": formE,
                    "groups": gr,
                    "spending": spendingR,
                    "msg": "Erro! Já existe um grupo com o mesmo nome",
                }

                if group_aux:  # pragma: no cover
                    return render(request, "dashboard/spending.html", self.item)

            except GroupSpending.DoesNotExist:
                if group_spending_form.is_valid():
                    form = group_spending_form.save(commit=False)
                    form.user = request.user
                    form.save()
                    return render(request, "dashboard/spending.html", self.item)

    def get(self, request):
        result = (
            Spending.objects.values("group")
            .filter(user=request.user, date__year=self.year, date__month=self.month)
            .annotate(Sum("value"))
        )

        gr1 = GroupSpending.objects.filter(user=request.user)

        gr = []
        for i in range(len(result)):  # pragma: no cover
            if result:
                gr.append(
                    {
                        "group": gr1[i].name,
                        "value": result[i]["value__sum"],
                    }
                )
            else:
                gr.append(
                    {
                        "group": gr1[i].name,
                        "value": 0,
                    }
                )
        spending = Spending.objects.filter(user=request.user).order_by("-id")
        paginator = Paginator(spending, 6)
        page = request.GET.get("page")
        spendingR = paginator.get_page(page)
        form1 = RegisterSpendingForm(user=request.user)
        form = RegisterGroupSpendingForm()
        formE = EditSpendingForm(user=request.user)
        valorR = 0
        p = Spending.objects.filter(
            user=request.user, date__year=self.year, date__month=self.month
        )
        for item in p:  # pragma: no cover
            valorR += item.value

        self.item = {
            "form1": form1,
            "spending": spendingR,
            "form": form,
            "formE": formE,
            "groups": gr,
            "result": valorR,
        }

        return render(request, "dashboard/spending.html", self.item)

class spendingDel(DeleteView, LoginRequiredMixin):
    model = Spending
    success_url = "/spending"
    login_url = "/signin"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class spendingEdit(View, LoginRequiredMixin):

    login_url = "/signin"

    def post(self, request, *args, **kwargs):

        spending = get_object_or_404(Spending, pk=kwargs.get("pk"))
        form = EditSpendingForm(request.POST, instance=spending, user=request.user)

        if form.is_valid():  # pragma: no cover
            spending = form.save(commit=False)
            spending.name = form.cleaned_data["name"]
            spending.value = form.cleaned_data["value"]
            spending.group = form.cleaned_data["group"]
            spending.date = form.cleaned_data["date"]
            spending.save()
            return redirect("spending")
        else:
            form = EditSpendingForm(instance=spending, user=request.user)
            return redirect("spending")


class signIn(View):
    def post(self, request):
        user_aux = User.objects.get(email=request.POST["email"])
        password = request.POST["password"]
        user = authenticate(request, username=user_aux.username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "dashboard/sign-in.html")

    def get(self, request):

        return render(request, "dashboard/sign-in.html")


class signUp(View):
    def post(self, request):
        user_form = RegisterUserForm(data=request.POST)
        try:
            user_aux = User.objects.get(email=request.POST["email"])
            form = RegisterUserForm()
            item = {
                "form": form,
                "msg": "Erro! Já existe um usuário com o mesmo e-mail",
            }

            if user_aux:
                return render(request, "dashboard/sign-up.html", item)

        except User.DoesNotExist:
            user = user_form.save(commit=False)
            user.password = make_password(user_form.cleaned_data["password"])
            user.save()
            return render(request, "dashboard/sign-in.html")

    def get(self, request):
        form = RegisterUserForm()
        item = {"form": form}

        return render(request, "dashboard/sign-up.html", item)


class exit(View, LoginRequiredMixin):

    login_url = "/signin"

    def get(self, request):
        logout(request)
        return redirect("/")
