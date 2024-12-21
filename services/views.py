import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Booking, Service
from .forms import ServiceForm, ServiceSearchForm
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create a service
@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.owner = request.user  # Assign the logged-in user as the owner
            service.save()
            # return redirect('service_list')
            # return redirect('services:service_list')
            return redirect(reverse('services:service_list'))
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})

def service_list(request):
    services = Service.objects.all()
    form = ServiceSearchForm(request.GET)  # Bind the form to GET parameters

    if form.is_valid():
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        # Filter based on the form inputs
        if category:
            services = services.filter(category=category)
        if min_price is not None:
            services = services.filter(price__gte=min_price)
        if max_price is not None:
            services = services.filter(price__lte=max_price)

    # Add pagination
    paginator = Paginator(services, 5)  # Show 5 services per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    return render(request, 'services/service_list.html', {
        'page_obj': page_obj,
        'form': form,
        # 'request': request,
    })




# Update a service
@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk, owner=request.user)  # Ensure the logged-in user is the owner
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            # return redirect('service_list')
            # return redirect('services:service_list')
            return redirect(reverse('services:service_list'))
            
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form})

# Delete a service
@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk, owner=request.user)  # Ensure the logged-in user is the owner
    if request.method == 'POST':
        service.delete()
        # return redirect('service_list')
        # return redirect('services:service_list')
        return redirect(reverse('services:service_list'))
    return render(request, 'services/service_confirm_delete.html', {'service': service})

# @login_required
# def process_payment(request, pk):
#     service = get_object_or_404(Service, pk=pk)

#     if request.method == 'POST':
#         try:
#             # Create a payment intent with updated parameters
#             intent = stripe.PaymentIntent.create(
#                 amount=int(service.price * 100),  # Convert to cents for Stripe
#                 currency='usd',
#                 payment_method=request.POST.get('payment_method_id'),
#                 # confirmation_method='manual',
#                 confirm=True,
#                 return_url=request.build_absolute_uri('/payment_success/')
#                 # automatic_payment_methods={
#                 #     "enabled": True,
#                 #     "allow_redirects": "never",  # Disable redirect-based payment methods
#                 # },
#             )

#             if intent['status'] == 'succeeded':
#                 service.is_paid = True
#                 service.save()
#                 return redirect('payment_success')

#             return render(request, 'services/payment_failure.html', {
#                 'error': f"Payment failed with status: {intent['status']}"
#             })

#         except stripe.error.CardError as e:
#             return render(request, 'services/payment_failure.html', {
#                 'error': f"Card Error: {str(e)}"
#             })

#         except stripe.error.InvalidRequestError as e:
#             return render(request, 'services/payment_failure.html', {
#                 'error': f"Invalid request: {str(e)}"
#             })

#         except Exception as e:
#             return render(request, 'services/payment_failure.html', {
#                 'error': f"An unexpected error occurred: {str(e)}"
#             })

#     return render(request, 'services/payment_form.html', {
#         'service': service,
#         'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
#     })
@login_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    booking, created = Booking.objects.get_or_create(client=request.user, service=service, defaults={'status': 'pending', 'payment_status': 'pending'})
    if created:
        messages.success(request, 'Booking created successfully.')
    return redirect(reverse('services:process_payment', kwargs={'booking_id': booking.id}))

def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    if booking.payment_status == 'success':
        messages.info(request, "This booking has already been paid for.")
        return redirect(reverse('users:client_dashboard'))

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': booking.service.title},
                    'unit_amount': int(booking.service.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('services:payment_success') + f'?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking.id}'
            ),
            cancel_url=request.build_absolute_uri(
                reverse('services:payment_failed') + f'?booking_id={booking.id}'
            ),
            # success_url=request.build_absolute_uri('/payment-success/') + f'?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking.id}',
            # cancel_url=request.build_absolute_uri('/payment-failed/') + f'?booking_id={booking.id}',
        )
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f"Payment failed: {e}")
        return redirect(reverse('users:client_dashboard')) 



# def payment_success(request):
#     return render(request, 'services/payment_success.html')

def payment_success(request):
    session_id = request.GET.get('session_id')
    booking_id = request.GET.get('booking_id')
    booking = get_object_or_404(Booking, id=booking_id)

    if session_id:
        booking.payment_status = 'success'
        booking.status = 'completed'
        booking.payment_id = session_id
        booking.save()
        messages.success(request, "Payment successful!")
    else:
        messages.error(request, "Payment verification failed.")
    # return redirect('client_dashboard')
    return redirect(reverse('users:client_dashboard'))

# def payment_failure(request):
#     return render(request, 'services/payment_failure.html')

def payment_failed(request):
    booking_id = request.GET.get('booking_id')
    booking = get_object_or_404(Booking, id=booking_id)
    booking.payment_status = 'failed'
    booking.status = 'failed'
    booking.save()
    messages.error(request, "Payment failed. Please try again.")
    # return redirect('client_dashboard')
    return redirect(reverse('users:client_dashboard'))

