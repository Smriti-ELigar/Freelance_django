from django.shortcuts import render, redirect
# from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import CustomUser
from services.models import Booking
from django.contrib.auth.decorators import login_required
from .decorators import freelancer_required, client_required
from services.models import Service  # Import your Service model
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse 

# Constants for role management
ROLE_FREELANCER = 'Freelancer'
ROLE_CLIENT = 'Client'

def home(request):
    # return render(request, 'users/home.html')
    # Determine the user's role and set the dashboard URL
    if request.user.is_authenticated:
        if request.user.role == ROLE_FREELANCER:  # Assuming `is_freelancer` is a boolean field on the user model
            dashboard_url = reverse('users:freelancer_dashboard')
        elif request.user.role == ROLE_CLIENT:
            dashboard_url = reverse('users:client_dashboard') 
    else:
        dashboard_url = None  # No dashboard for anonymous users

    return render(request, 'users/home.html', {'dashboard_url': dashboard_url})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = request.POST.get('role')
            user.is_active = True  # Require email verification
            user.save()

            # Send email verification
            token = str(uuid.uuid4())
            send_mail(
                'Verify your email',
                f'Use this link to verify your email: http://127.0.0.1:8000/verify/{token}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect(reverse('users:login'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})



def verify_email(request, token):
    user = get_object_or_404(CustomUser, email_verification_token=token)
    if user:
        user.is_verified = True
        user.email_verification_token = None
        user.save()
        messages.success(request, "Your email has been successfully verified!")
        return redirect(reverse('users:login'))
    else:
        messages.error(request, "Invalid or expired token. Please try again.")
        return redirect(reverse('users:resend_verification_email'))

    
def resend_verification_email(request):
    if request.method == 'POST':
        user = request.user
        if user and not user.is_verified:
            user.email_verification_token = uuid.uuid4()
            user.save()
            send_mail(
                "Verify Your Email",
                f"Please click the link below to verify your email:\n"
                f"http://example.com/verify-email/{user.email_verification_token}/",
                "no-reply@example.com",
                [user.email],
            )
            messages.success(request, "Verification email has been resent!")
        return redirect('home')
    return render(request, 'users/resend_verification_email.html')
    



@login_required
def dashboard_redirect(request):
    """Redirect user to their respective dashboard based on role."""
    if request.user.role == ROLE_FREELANCER:
        return redirect('users:freelancer_dashboard')  # Include namespace
    elif request.user.role == ROLE_CLIENT:
        return redirect('users:client_dashboard')  # Include namespace
    else:
        # Log unexpected roles for debugging and fallback to a generic dashboard
        print(f"Unexpected or undefined role: {request.user.role}")
        return render(request, 'users/dashboard.html', {'role': request.user.role})

@login_required
@freelancer_required
def freelancer_dashboard(request):
    """Freelancer Dashboard"""
    # Filter only completed bookings to calculate earnings
    total_earnings = Booking.objects.filter(service__owner=request.user, status='completed') \
                                     .aggregate(Sum('service__price'))['service__price__sum'] or 0

    # services = Service.objects.filter(owner=request.user).prefetch_related('category')
    services = Service.objects.filter(owner=request.user) # Removed prefetch_related('category')

    return render(request, 'users/freelancer_dashboard.html', {
        'services': services,
        'total_earnings': total_earnings,
        'user_name':  request.user.username,
    })   

@login_required
@client_required
def client_dashboard(request):
    """Client Dashboard"""
    # Filter completed bookings for calculating total spent
    bookings = Booking.objects.filter(client=request.user, status='completed').select_related('service')

    total_spent = bookings.aggregate(Sum('service__price'))['service__price__sum'] or 0

    return render(request, 'users/client_dashboard.html', {
        'bookings': bookings,
        'total_spent': total_spent,
        'user_name':  request.user.username,
    })

def custom_permission_denied_view(request, exception=None):
    return render(request, 'users/403.html', status=403)
