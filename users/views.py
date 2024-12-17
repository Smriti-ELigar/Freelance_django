from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .decorators import freelancer_required, client_required

def home(request):
    return render(request, 'users/home.html')

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
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})



def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        user.is_active = True
        user.email_verification_token = ''
        user.save()
        return HttpResponse("Email verified successfully!")
    except CustomUser.DoesNotExist:
        return HttpResponse("Invalid token!")
    

@login_required
def dashboard_redirect(request):
    print(f"User Role: {request.user.role}")
    if request.user.role == 'Freelancer':
        return redirect('freelancer_dashboard')
    elif request.user.role == 'Client':
        return redirect('client_dashboard')
    else:
        return HttpResponse("Invalid role. Please contact support.")



@login_required
@freelancer_required
def freelancer_dashboard(request):
    return render(request, 'users/freelancer_dashboard.html')

@login_required
@client_required
def client_dashboard(request):
    return render(request, 'users/client_dashboard.html')






















# render and redirect are used to render HTML templates and redirect users to different views.
# login is used to log in a user.
# CustomUserCreationForm is a custom form for user creation (assumed to be defined elsewhere).
# send_mail is used to send emails.
# settings is used to access Django settings.
# uuid is used to generate unique identifiers.
# Method check:
# The function starts by checking if the request method is POST. If so, it means the user has submitted the signup form.
# Form handling:
# form = CustomUserCreationForm(request.POST): Initializes the form with the POST data.
# if form.is_valid(): Checks if the form data is valid.
# User creation and email verification:
# user = form.save(commit=False): Saves the form data to create a user instance, but doesn't commit it to the database yet.
# user.is_active = False: Sets the is_active attribute of the user to False, indicating the user account is inactive until email verification.
# user.save(): Saves the user to the database.
# Token generation and email sending:
# token = str(uuid.uuid4()): Generates a unique token for email verification.
# send_mail(): Sends an email to the user with a verification link containing the token.
# Redirect:
# return redirect('login'): Redirects the user to the login page after the form submission.
# Form initialization for GET request:
# If the request method is not POST, it initializes an empty form: form = CustomUserCreationForm().
# Render template:
# Finally, it renders the signup template with the form: return render(request, 'users/signup.html', {'form': form}).

# Defines a function verify_email that takes request and token as parameters. request is the HTTP request object, and token is the verification token passed in the URL.Try Block:

# user = CustomUser.objects.get(email_verification_token=token): Attempts to find a CustomUser instance with a matching email_verification_token. If no such user exists, it raises a CustomUser.DoesNotExist exception.

# user.is_active = True: Sets the is_active attribute of the user to True, indicating the user account is now active.

# user.email_verification_token = '': Clears the email_verification_token field, as it is no longer needed.

# user.save(): Saves the changes to the user object in the database.

# return HttpResponse("Email verified successfully!"): Returns an HTTP response indicating successful email verification.

# Except Block:

# Catches the CustomUser.DoesNotExist exception if no user with the provided token is found.

# return HttpResponse("Invalid token!"): Returns an HTTP response indicating that the token is invalid.