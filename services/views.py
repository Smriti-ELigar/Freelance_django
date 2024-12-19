import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Service
from .forms import ServiceForm, ServiceSearchForm

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
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})



def service_list(request):
    services = Service.objects.all()
    form = ServiceSearchForm(request.GET)  # Bind the form to GET parameters

    if form.is_valid():
        title = form.cleaned_data.get('title')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        # Filter based on the form inputs
        if title:
            services = services.filter(title__icontains=title)
        if category:
            services = services.filter(category=category)
        if min_price is not None:
            services = services.filter(price__gte=min_price)
        if max_price is not None:
            services = services.filter(price__lte=max_price)

    return render(request, 'services/service_list.html', {
        'services': services,
        'form': form,
    })


# Update a service
@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk, owner=request.user)  # Ensure the logged-in user is the owner
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form})

# Delete a service
@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk, owner=request.user)  # Ensure the logged-in user is the owner
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'services/service_confirm_delete.html', {'service': service})

# @login_required
# def process_payment(request, pk):
#     service = get_object_or_404(Service, pk=pk)
   


#     if request.method == 'POST':
#         # Create a payment intent
#         intent = stripe.PaymentIntent.create(
#             amount=int(service.price * 100),  # Convert to cents for Stripe
#             currency='usd',
#             payment_method=request.POST.get('payment_method_id'),
#             confirmation_method='manual',
#             confirm=True,
#         )

#         if intent['status'] == 'succeeded':
#             service.is_paid = True
#             service.save()
#             return redirect('payment_success')
#         # print("Stripe Publishable Key:", settings.STRIPE_PUBLIC_KEY)


#         return render(request, 'services/payment_failure.html')


#     return render(request, 'services/payment_form.html', {
#         'service': service,
#         'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
#     })
@login_required
def process_payment(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        try:
            # Create a payment intent with updated parameters
            intent = stripe.PaymentIntent.create(
                amount=int(service.price * 100),  # Convert to cents for Stripe
                currency='usd',
                payment_method=request.POST.get('payment_method_id'),
                # confirmation_method='manual',
                confirm=True,
                return_url=request.build_absolute_uri('/payment_success/')
                # automatic_payment_methods={
                #     "enabled": True,
                #     "allow_redirects": "never",  # Disable redirect-based payment methods
                # },
            )

            if intent['status'] == 'succeeded':
                service.is_paid = True
                service.save()
                return redirect('payment_success')

            return render(request, 'services/payment_failure.html', {
                'error': f"Payment failed with status: {intent['status']}"
            })

        except stripe.error.CardError as e:
            return render(request, 'services/payment_failure.html', {
                'error': f"Card Error: {str(e)}"
            })

        except stripe.error.InvalidRequestError as e:
            return render(request, 'services/payment_failure.html', {
                'error': f"Invalid request: {str(e)}"
            })

        except Exception as e:
            return render(request, 'services/payment_failure.html', {
                'error': f"An unexpected error occurred: {str(e)}"
            })

    return render(request, 'services/payment_form.html', {
        'service': service,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })




def payment_success(request):
    return render(request, 'services/payment_success.html')


def payment_failure(request):
    return render(request, 'services/payment_failure.html')



''' 
render: Renders a template with a context.

get_object_or_404: Retrieves an object from the database or returns a 404 error if not found.

redirect: Redirects to a different URL.

login_required: Ensures that the view can only be accessed by authenticated users.

Service: The model representing the service entity.

ServiceForm: The form used to create and update services.
This view handles the creation of a new service.

Only authenticated users can access it (@login_required).

If the request method is POST, it processes the submitted form.

If the form is valid, it assigns the logged-in user as the owner of the service and saves it.

Redirects to the service_list view after saving.

If the request method is not POST, it displays an empty form.
This view lists all the services.

It retrieves all service objects from the database and renders them in the service_list.html template.
This view handles updating an existing service.

Only the owner of the service can update it (get_object_or_404 ensures the logged-in user is the owner).

If the request method is POST, it processes the submitted form with the instance of the existing service.

If the form is valid, it saves the changes and redirects to the service_list view.

If the request method is not POST, it displays the form pre-filled with the service's data.
This view handles deleting a service.

Only the owner of the service can delete it (get_object_or_404 ensures the logged-in user is the owner).

If the request method is POST, it deletes the service and redirects to the service_list view.

If the request method is not POST, it displays a confirmation page.

In summary, these views provide a complete CRUD (Create, Read, Update, Delete) interface for managing services in a Django application. 
Each view ensures that only authenticated users can create, update, or delete services and that only the owner of a service can update or delete it.
'''