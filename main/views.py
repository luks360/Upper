from django.shortcuts import redirect, get_object_or_404, render
from main.forms import (
    EditProfitsForm,
    RegisterUserForm,
    RegisterGroupProfitsForm,
    RegisterProfitsForm,
    RegisterSpendingForm,
    EditSpendingForm,
    RegisterGroupSpendingForm,
)
from django.contrib.auth import authenticate, login, logout
from main.models import User, GroupProfits, Profits, GroupSpending, Spending
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from datetime import datetime
from django.core.paginator import Paginator

# Create your views here.


def home(request):

    return render(request, "main/index.html")


def dashboard(request):
    if request.user.is_authenticated == False:
        return redirect("signin")

    currentDateTime = datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    month = date.strftime("%m")

    mes_profits = (
        Profits.objects.filter(user=request.user, date__year=year)
        .dates("date", "year")
        .values("date")
        .annotate(Sum("value"))
    )

    mes_spending = (
        Spending.objects.filter(user=request.user, date__year=year)
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
    p = Profits.objects.filter(user=request.user, date__month=month, date__year=year)
    for item in p:  # pragma: no cover
        profitsT += item.value

    spendingT = 0
    s = Spending.objects.filter(user=request.user, date__month=month, date__year=year)
    for item in s:  # pragma: no cover
        spendingT += item.value

    profitsTA = 0
    pa = Profits.objects.filter(
        user=request.user, date__month=date.month - 1, date__year=year
    )
    for item in pa:  # pragma: no cover
        profitsTA += item.value

    spendingTA = 0
    sa = Spending.objects.filter(
        user=request.user, date__month=date.month - 1, date__year=year
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


def profits(request):
    if request.user.is_authenticated == False:
        return redirect("signin")

    currentDateTime = datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    month = date.strftime("%m")

    result = (
        Profits.objects.values("group")
        .filter(user=request.user, date__year=year, date__month=month)
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

    count = 0

    if request.method == "POST":
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
                    "count": count,
                    "msg": "Erro! Já existe um grupo com o mesmo nome",
                }

                if group_aux:  # pragma: no cover
                    return render(request, "dashboard/profits.html", item)

            except GroupProfits.DoesNotExist:
                if group_profits_form.is_valid():
                    form = group_profits_form.save(commit=False)
                    form.user = request.user
                    form.save()

    form1 = RegisterProfitsForm(user=request.user)
    form = RegisterGroupProfitsForm()
    formE = EditProfitsForm(user=request.user)
    valorR = 0
    p = Profits.objects.filter(user=request.user, date__year=year, date__month=month)
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


@login_required
def profitDel(request, id):
    profits = Profits.objects.filter(id=id).first()
    profits.delete()
    return redirect("profits")


@login_required
def profitEdit(request, id):
    profit = get_object_or_404(Profits, pk=id)
    form = EditProfitsForm(instance=profit, user=request.user)

    if request.method == "POST":
        form = EditProfitsForm(request.POST, instance=profit, user=request.user)

        if form.is_valid():  # pragma: no cover
            profit = form.save(commit=False)
            profit.name = form.cleaned_data["name"]
            profit.value = form.cleaned_data["value"]
            profit.group = form.cleaned_data["group"]
            profit.date = form.cleaned_data["date"]
            profit.save()
            return redirect("profits")

    return redirect("profits")


def spending(request):
    if request.user.is_authenticated == False:
        return redirect("signin")

    currentDateTime = datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    month = date.strftime("%m")

    result = (
        Spending.objects.values("group")
        .filter(user=request.user, date__year=year, date__month=month)
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

    spendings = Spending.objects.filter(user=request.user).order_by("-id")
    paginator = Paginator(spendings, 6)
    page = request.GET.get("page")
    spendingsR = paginator.get_page(page)

    count = 0

    if request.method == "POST":
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
                item = {
                    "form": form,
                    "form1": form1,
                    "formE": formE,
                    "groups": gr,
                    "spending": spendingsR,
                    "count": count,
                    "msg": "Erro! Já existe um grupo com o mesmo nome",
                }

                if group_aux:
                    return render(request, "dashboard/spending.html", item)

            except GroupSpending.DoesNotExist:
                if group_spending_form.is_valid():
                    form = group_spending_form.save(commit=False)
                    form.user = request.user
                    form.save()
                    return redirect("spending")

    form1 = RegisterSpendingForm(user=request.user)
    form = RegisterGroupSpendingForm()
    formE = EditSpendingForm(user=request.user)
    valorR = 0

    s = Spending.objects.filter(user=request.user, date__year=year, date__month=month)
    for item in s:  # pragma: no cover
        valorR += item.value

    item = {
        "form1": form1,
        "spending": spendingsR,
        "form": form,
        "formE": formE,
        "groups": gr,
        "result": valorR,
    }
    return render(request, "dashboard/spending.html", item)


@login_required
def spendingDel(request, id):
    spending = Spending.objects.filter(id=id).first()
    spending.delete()
    return redirect("spending")


@login_required
def spendingEdit(request, id):
    spending = get_object_or_404(Spending, pk=id)
    form = EditSpendingForm(instance=spending, user=request.user)

    if request.method == "POST":
        form = EditSpendingForm(request.POST, instance=spending, user=request.user)

        if form.is_valid():  # pragma: no cover
            spending = form.save(commit=False)
            spending.name = form.cleaned_data["name"]
            spending.value = form.cleaned_data["value"]
            spending.group = form.cleaned_data["group"]
            spending.date = form.cleaned_data["date"]
            spending.save()
            return redirect("spending")

    return redirect("spending")


def signIn(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":  # pragma: no cover
        user_aux = User.objects.get(email=request.POST["email"])
        password = request.POST["password"]
        user = authenticate(request, username=user_aux.username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")

    return render(request, "dashboard/sign-in.html")


def signUp(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":  # pragma: no cover
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

    form = RegisterUserForm()
    item = {"form": form}

    return render(
        request,
        "dashboard/sign-up.html",
        item,
    )


@login_required
def exit(request):
    logout(request)
    return redirect("/")
