from django.urls import path
from django.contrib.auth.views import LoginView
from .views import home, signup, verify_email

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('verify/<str:token>/', verify_email, name='verify_email'),
    path('', home, name='home'), # Add this line
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'), 
]
