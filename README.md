# Freelance Marketplace

A robust freelance marketplace web application built using Django, allowing users to register as freelancers or clients, browse services, and make bookings with integrated payment processing.

## Features  

### 1. User Registration and Authentication
- Email-based signup system with email verification.  
- Unique tokens for account activation.  
- Secure login system for freelancers and clients.  

### 2. Service Listings 
- Freelancers can:  
  - Create new service listings.  
  - Edit or delete existing listings.  
- Clients can:  
  - Browse services by category or search for specific ones.  

### 3. Booking and Payment 
- Clients can book a freelancer’s service.  
- Payments processed via Stripe.  
- Confirmation page displayed upon successful payment.  

### 4. Dashboards  
- **Freelancer Dashboard**:  
  - Manage service listings.  
  - View bookings and payment history.  
- **Client Dashboard**:  
  - View booked services.  
  - Access payment history.  


## Technologies Used  

- **Backend**: Django  
- **Frontend**: HTML, CSS, JavaScript  
- **Payment Gateway**: Stripe  
- **Database**: SQLite (default, replaceable with PostgreSQL/MySQL)  

## Security Features  

- Email-based verification with unique token generation.  
- Secure password storage using Django's `PBKDF2` password hasher.  
- CSRF protection enabled by default in Django.  
