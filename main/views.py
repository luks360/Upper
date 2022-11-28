from django.shortcuts import redirect, render
from main.forms import RegisterUserForm
from django.contrib.auth import authenticate, login, logout
from main.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

# Create your views here.
def home(request):
    
    return render(request, 'main/index.html')

def dashboard(request):
    if request.user.is_authenticated == False:
        return redirect('signin')

    return render(request, 'dashboard/dashboard.html')

def signIn(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        user_aux = User.objects.get(email=request.POST['email'])
        password = request.POST["password"]
        user = authenticate(request, username=user_aux.username, password=password)
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