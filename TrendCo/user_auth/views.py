from django.shortcuts import render
from .forms  import RegistrationForm

# Create your views here.
def register(request):
    form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request,'user_auth/register.html',context)

def login(request):
    return render(request,'user_auth/login.html')

def logout(request):
    return render(request,'user_auth/logout.html')