from django.shortcuts import render,redirect, HttpResponse
from .forms  import RegistrationForm
from .models import CustomUser
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required


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
            # account activation 
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('user_auth/account_activation.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
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


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations,Account Activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid Activation Link')
        return redirect('register')