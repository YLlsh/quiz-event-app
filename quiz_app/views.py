from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


from django.contrib import messages
# Create your views here.
def home(request):

    return render(request,'home.html')

def quiz_list(request):

    return render(request,'quiz_list.html')

def question(request):

    return render(request,'questions.html')

def score(request):

    return render(request,'score.html')


def log_in(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password =password)

        if user is not None:
            login(request, user)
            return redirect('admin_dash')
            messages.error(request,'matched')

        else:
            messages.error(request,'username or password not match')
            return redirect('login')

    return render(request,'login.html')


def log_out(request):
    logout(request)

    return redirect('login')


def admin_dash(request):

    return render(request,'admin_dash.html')

