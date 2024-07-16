from django.shortcuts import render,redirect
from .forms  import RegistrationForm
from .models import CustomUser
from django.contrib import messages, auth
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            contact_number = form.cleaned_data['contact_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.objects.create_user(
                first_name=first_name, last_name=last_name, email=email,
                password=password
            )
            user.contact_number = contact_number
            user.save()
            messages.success(request,'You are registered Successfully.')
            return redirect('register')
    else:
        form = RegistrationForm()       
    context = {
        'form': form
    }
    return render(request,'user_auth/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password = password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'Logged in successful')
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')
    return render(request,'user_auth/login.html')

def logout(request):
    return render(request,'user_auth/logout.html')