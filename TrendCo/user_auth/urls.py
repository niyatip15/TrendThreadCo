from django.urls import path 
from . import views
urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
     path('', views.dashboard, name='dashboard'),
    path('logout/',views.logout, name='logout') ,
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    
    path('my_orders/',views.myOrders,name='my_orders'),
    # path('edit-profile/',views.editProfile,name='edit-profile'),
    # path('change-passwoed/',views.changePassword,name='change-password')
]