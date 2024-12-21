from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    home,
    signup,
    verify_email,
    resend_verification_email,
    freelancer_dashboard,
    client_dashboard,
    dashboard_redirect,
    custom_permission_denied_view,
)

app_name = 'users'  # This defines the namespace for this app's URLs.

urlpatterns = [
    # Public URLs
    path('', home, name='home'),  # Home view
    path('signup/', signup, name='signup'),  # Signup view
    path('verify/<str:token>/', verify_email, name='verify_email'),  # Email verification
    path('resend_verification_email/', resend_verification_email, name='resend_verification_email'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),  # Login view

    # Authenticated redirects
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),

    # Role-specific dashboards
    path('freelancer_dashboard/', freelancer_dashboard, name='freelancer_dashboard'),
    path('client_dashboard/', client_dashboard, name='client_dashboard'),
   
]
