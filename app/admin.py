from django.contrib import admin
from .models import Therapist, Service, Appointment, Payment, CustomerProfile, Availability

# Therapist Admin
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'available')
    search_fields = ('name', 'specialty')
    list_filter = ('available',)
    ordering = ('name',)  # Sorts therapists by name

# Service Admin
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    search_fields = ('name',)
    ordering = ('name',)

# Appointment Admin
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'therapist', 'service', 'date', 'time', 'status', 'payment_status')
    search_fields = ('client__username', 'therapist__name', 'service__name')
    list_filter = ('status', 'payment_status', 'date', 'therapist')  # Added therapist filter
    ordering = ('-date', 'time')  # Orders by most recent date

# Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'payment_method', 'date')
    search_fields = ('appointment__client__username', 'transaction_id')
    list_filter = ('payment_method',)
    ordering = ('-date',)  # Orders by most recent payments

# Customer Profile Admin
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'loyalty_points')
    search_fields = ('user__username',)
    ordering = ('user',)  # Orders alphabetically by user

# Availability Admin
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'date')
    search_fields = ('therapist__name',)
    list_filter = ('date', 'therapist')  # Added therapist filter
    ordering = ('date',)  # Orders by date

# Registering Models
admin.site.register(Therapist, TherapistAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(Availability, AvailabilityAdmin)
