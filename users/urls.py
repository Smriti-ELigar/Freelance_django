from django.urls import path
from .views import home, signup, verify_email

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('verify/<str:token>/', verify_email, name='verify_email'),
    path('', home, name='home'), # Add this line
]
