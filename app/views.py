from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from .models import Appointment, Therapist, Service, Payment
from django.shortcuts import get_object_or_404
from .forms import TherapistForm, ServiceForm, AppointmentForm, PaymentForm, CustomerProfileForm, AvailabilityForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, "Your account has been created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'app/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')  
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def home(request):
    return render(request, 'app/home.html')  

def about(request):
    return render(request, 'app/about.html')

def services(request):
    services_list = Service.objects.all()  
    return render(request, 'app/services.html', {'services': services_list})

def booking(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to make a booking.")
        return redirect('login')

    therapists = Therapist.objects.filter(available=True)
    services = Service.objects.all()  
    return render(request, 'app/booking.html', {'therapists': therapists, 'services': services})

def confirm_booking(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to confirm a booking.")
        return redirect('login')

    if request.method == 'POST':
        service_id = request.POST.get('service')
        therapist_id = request.POST.get('therapist')
        date = request.POST.get('date')
        time = request.POST.get('time')


        if not service_id or not therapist_id or not date or not time:
            messages.error(request, "Please fill in all the fields.")
            return redirect('booking')


        therapist = get_object_or_404(Therapist, id=therapist_id)
        if not therapist.available:
            messages.error(request, f"{therapist.name} is not available.")
            return redirect('booking')


        appointment = Appointment.objects.create(
            client=request.user,
            service_id=service_id,
            therapist_id=therapist_id,
            date=date,
            time=time,
        )

        messages.success(request, f"Appointment booked successfully with {therapist.name} for {appointment.date} at {appointment.time}.")

        context = {
            'appointment': appointment,
        }

        return render(request, 'app/confirm_booking.html', context)
    else:
        return redirect('home')

def process_payment(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to make a payment.")
        return redirect('login')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')
        appointment_id = request.POST.get('appointment_id')

        if not payment_method or not transaction_id or not appointment_id:
            messages.error(request, "Please provide all required payment details.")
            return redirect('payment')

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found.")
            return redirect('home')

        success = True

        if success:
            appointment.payment_status = True
            appointment.save()

            Payment.objects.create(
                appointment=appointment,
                amount=appointment.service.price,
                payment_method=payment_method,
                transaction_id=transaction_id,
            )

            messages.success(request, f"Payment processed successfully for your appointment with {appointment.therapist.name}.")
            return redirect('appointments_list')  
        else:
            messages.error(request, "Payment processing failed.")
            return redirect('payment')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('home')


def manage_all_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')  

        if action == 'therapist':
            form = TherapistForm(request.POST, request.FILES, prefix='therapist')
            if form.is_valid():
                form.save()
                messages.success(request, "Therapist saved successfully.")
            else:
                messages.error(request, "Therapist form contains errors.")

        elif action == 'service':
            form = ServiceForm(request.POST, request.FILES, prefix='service')
            if form.is_valid():
                form.save()
                messages.success(request, "Service saved successfully.")
            else:
                messages.error(request, "Service form contains errors.")

        elif action == 'appointment':
            form = AppointmentForm(request.POST, prefix='appointment')
            if form.is_valid():
                form.save()
                messages.success(request, "Appointment booked successfully.")
            else:
                messages.error(request, "Appointment form contains errors.")

        elif action == 'payment':
            form = PaymentForm(request.POST, prefix='payment')
            if form.is_valid():
                form.save()
                messages.success(request, "Payment processed successfully.")
            else:
                messages.error(request, "Payment form contains errors.")

        elif action == 'customer_profile':
            form = CustomerProfileForm(request.POST, prefix='customer_profile')
            if form.is_valid():
                form.save()
                messages.success(request, "Customer profile updated successfully.")
            else:
                messages.error(request, "Customer profile form contains errors.")

        elif action == 'availability':
            form = AvailabilityForm(request.POST, prefix='availability')
            if form.is_valid():
                form.save()
                messages.success(request, "Availability updated successfully.")
            else:
                messages.error(request, "Availability form contains errors.")

        return redirect('manage_all')

    else:
        therapist_form = TherapistForm(prefix='therapist')
        service_form = ServiceForm(prefix='service')
        appointment_form = AppointmentForm(prefix='appointment')
        payment_form = PaymentForm(prefix='payment')
        customer_profile_form = CustomerProfileForm(prefix='customer_profile')
        availability_form = AvailabilityForm(prefix='availability')

    return render(request, 'app/manage_all.html', {
        'therapist_form': therapist_form,
        'service_form': service_form,
        'appointment_form': appointment_form,
        'payment_form': payment_form,
        'customer_profile_form': customer_profile_form,
        'availability_form': availability_form,
    })
