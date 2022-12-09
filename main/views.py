from decimal import Decimal
from django.shortcuts import redirect, get_object_or_404, render
from main.forms import EditProfitsForm, RegisterUserForm, RegisterGroupProfitsForm, RegisterProfitsForm, RegisterSpendingForm, EditSpendingForm, RegisterGroupSpendingForm
from django.contrib.auth import authenticate, login, logout
from main.models import User, GroupProfits, Profits, GroupSpending, Spending
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from datetime import datetime
from django.core.paginator import Paginator

# Create your views here.


def home(request):

    return render(request, 'main/index.html')


def dashboard(request):
    if request.user.is_authenticated == False:
        return redirect('signin')

    mes_profits = Profits.objects.filter(user=request.user).dates('date', 'year').values(
        'date').annotate(Sum('value'))

    mes_spending = Spending.objects.filter(user=request.user).dates('date', 'year').values(
        'date').annotate(Sum('value'))

    labels = []
    values = []
    labels1 = []
    values1 = []

    for data in range(len(mes_profits)):
        labels.append(mes_profits[data]['date'].strftime("%B"))
        values.append(float(mes_profits[data]['value__sum']))

    for data in range(len(mes_spending)):
        labels1.append(mes_spending[data]['date'].strftime("%B"))
        values1.append(float(mes_spending[data]['value__sum']))

    print(mes_profits)
    print(values)
    return render(request, 'dashboard/dashboard.html', {'date': labels, 'value': values, 'value1': values1})


def profile(request):
    if request.user.is_authenticated == False:
        return redirect('signin')

    return render(request, 'dashboard/profile.html')


def profits(request):
    if request.user.is_authenticated == False:
        return redirect('signin')

    result = Profits.objects.values("group").filter(
        user=request.user).annotate(Sum("value"))
    gr = GroupProfits.objects.filter(user=request.user)

    profits = Profits.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(profits, 6)
    page = request.GET.get('page')
    profitsR = paginator.get_page(page)

    count = 0

    if request.method == "POST":
        group_profits_form = RegisterGroupProfitsForm(data=request.POST)
        profits_form = RegisterProfitsForm(request.POST, user=request.user)

        if profits_form:
            if profits_form.is_valid():
                form = profits_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('profits')

        if group_profits_form:
            try:
                group_aux = GroupProfits.objects.get(name=request.POST['name'])
                form = RegisterGroupProfitsForm()
                formE = EditProfitsForm(user=request.user)
                form1 = RegisterProfitsForm(user=request.user)
                item = {
                    'form': form,
                    'form1': form1,
                    'formE': formE,
                    'groups': gr,
                    'profits': profitsR,
                    'count': count,
                    'msg': 'Erro! Já existe um grupo com o mesmo nome',
                }

                if group_aux:
                    return render(request, 'dashboard/profits.html', item)

            except GroupProfits.DoesNotExist:
                if group_profits_form.is_valid():
                    form = group_profits_form.save(commit=False)
                    form.user = request.user
                    form.save()

    form1 = RegisterProfitsForm(user=request.user)
    form = RegisterGroupProfitsForm()
    formE = EditProfitsForm(user=request.user)
    valorR = 0
    for item in profitsR:
        valorR += item.value

    mes_profits = Profits.objects.dates('date', 'month').values(
        'date').annotate(Sum('value'))

    print(mes_profits)

    item = {
        'form1': form1,
        'profits': profitsR,
        'form': form,
        'formE': formE,
        'groups': gr,
        'result': valorR,
        'mes': mes_profits
    }
    print(result)
    return render(request, 'dashboard/profits.html', item)


@login_required
def profitDel(request, id):
    profits = Profits.objects.filter(id=id).first()
    profits.delete()
    return redirect('profits')


@login_required
def profitEdit(request, id):
    profit = get_object_or_404(Profits, pk=id)
    form = EditProfitsForm(instance=profit, user=request.user)

    print(request.method)
    if request.method == 'POST':
        form = EditProfitsForm(
            request.POST, instance=profit, user=request.user
        )

        print(form.is_valid())
        if (form.is_valid()):
            profit = form.save(commit=False)
            profit.name = form.cleaned_data['name']
            profit.value = form.cleaned_data['value']
            profit.group = form.cleaned_data['group']
            profit.date = form.cleaned_data['date']
            profit.save()
            return redirect('profits')

    return redirect('profits')


def spending(request):
    if request.user.is_authenticated == False:
        return redirect('signin')

    result = Spending.objects.values("group").filter(
        user=request.user).annotate(Sum("value"))
    gr = GroupSpending.objects.filter(user=request.user)

    spendings = Spending.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(spendings, 6)
    page = request.GET.get('page')
    spendingsR = paginator.get_page(page)

    count = 0

    if request.method == "POST":
        group_spending_form = RegisterGroupSpendingForm(data=request.POST)
        spending_form = RegisterSpendingForm(request.POST, user=request.user)

        if spending_form:
            if spending_form.is_valid():
                form = spending_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('spending')

        if group_spending_form:
            try:
                group_aux = GroupSpending.objects.get(
                    name=request.POST['name'])
                form = RegisterGroupSpendingForm()
                formE = EditSpendingForm(user=request.user)
                form1 = RegisterSpendingForm(user=request.user)
                item = {
                    'form': form,
                    'form1': form1,
                    'formE': formE,
                    'groups': gr,
                    'spending': spendingsR,
                    'count': count,
                    'msg': 'Erro! Já existe um grupo com o mesmo nome',
                }

                if group_aux:
                    return render(request, 'dashboard/spending.html', item)

            except GroupSpending.DoesNotExist:
                if group_spending_form.is_valid():
                    form = group_spending_form.save(commit=False)
                    form.user = request.user
                    form.save()
                    return redirect('spending')

    form1 = RegisterSpendingForm(user=request.user)
    form = RegisterGroupSpendingForm()
    formE = EditSpendingForm(user=request.user)
    valorR = 0
    for item in spendingsR:
        valorR += item.value

    mes_spending = Spending.objects.dates('date', 'month').values(
        'date').annotate(Sum('value'))

    item = {
        'form1': form1,
        'spending': spendingsR,
        'form': form,
        'formE': formE,
        'groups': gr,
        'result': valorR,
        'mes': mes_spending
    }
    return render(request, 'dashboard/spending.html', item)


@login_required
def spendingDel(request, id):
    spending = Spending.objects.filter(id=id).first()
    spending.delete()
    return redirect('spending')


@login_required
def spendingEdit(request, id):
    spending = get_object_or_404(Spending, pk=id)
    form = EditSpendingForm(instance=spending, user=request.user)

    if request.method == 'POST':
        form = EditSpendingForm(
            request.POST, instance=spending, user=request.user
        )

        if (form.is_valid()):
            spending = form.save(commit=False)
            spending.name = form.cleaned_data['name']
            spending.value = form.cleaned_data['value']
            spending.group = form.cleaned_data['group']
            spending.date = form.cleaned_data['date']
            spending.save()
            return redirect('spending')

    return redirect('spending')


def signIn(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        user_aux = User.objects.get(email=request.POST['email'])
        password = request.POST["password"]
        user = authenticate(
            request, username=user_aux.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, "dashboard/sign-in.html")


def signUp(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        user_form = RegisterUserForm(data=request.POST)
        try:
            user_aux = User.objects.get(email=request.POST['email'])
            form = RegisterUserForm()
            item = {
                'form': form,
                'msg': 'Erro! Já existe um usuário com o mesmo e-mail',
            }

            if user_aux:
                return render(request, 'dashboard/sign-up.html', item)

        except User.DoesNotExist:
            user = user_form.save(commit=False)
            user.password = make_password(user_form.cleaned_data['password'])
            user.save()

    form = RegisterUserForm()
    item = {
        'form': form
    }

    return render(request, 'dashboard/sign-up.html', item, )


@login_required
def exit(request):
    logout(request)
    return redirect('/')
