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
from cart.models import *
from orders.models import *
from cart.views import _cart_id

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
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItems.objects.filter(cart=cart)
                
                for item in cart_items:
                    existing_item = CartItems.objects.filter(user=user, product=item.product).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.save()
                        item.delete()
                    else:
                        item.user = user
                        item.cart = None
                        item.save()
                
                cart.delete()  # Delete the guest cart after merging
            except Cart.DoesNotExist:
                pass
            
            auth.login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    
    return render(request, 'user_auth/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')



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
    
    
@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id, is_ordered = True)
    order_count = orders.count()
    context = {
        'orders':order_count
    }
    return render(request, 'user_auth/dashboard.html',context)

def myOrders(request):
    my_orders = Order.objects.filter(user = request.user,is_ordered=True).order_by('-created_at')
    print(my_orders,'heya')
    context = {
        'orders':my_orders
    }
    return render(request,'user_auth/myorders.html',context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.objects.filter(email = email).exists():
            user = CustomUser.objects.get(email = email)
            # Reset password email 
            current_site = get_current_site(request)
            mail_subject = 'Reset Password'
            message = render_to_string('user_auth/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')
    return render(request,'user_auth/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
    
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'user_auth/resetpassword.html')