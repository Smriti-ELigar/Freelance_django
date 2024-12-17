from django.urls import path
from django.contrib.auth.views import LoginView
from .views import home, signup, verify_email, client_dashboard, freelancer_dashboard
from users import views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('verify/<str:token>/', verify_email, name='verify_email'),
    path('', home, name='home'), # Add this line
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'), 
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('dashboard/freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
    # path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('freelancer_dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard')
]   
