from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Therapist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    specialty = models.CharField(max_length=100, help_text="Specialization of the therapist")
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='therapists/', null=True, blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField(help_text="Duration of the service")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='services/', null=True, blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')
    payment_status = models.BooleanField(default=False, help_text="Has payment been made?")
    reservation_fee = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)

    class Meta:
        unique_together = ('client', 'therapist', 'date', 'time')  # Prevents double-booking

    def __str__(self):
        return f"{self.client.username} - {self.service.name} on {self.date} at {self.time}"


class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=[('e_wallet', 'E-Wallet')])
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment for {self.appointment} - {self.amount} {self.payment_method}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Availability(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateField()
    available_slots = models.JSONField(help_text="Available time slots for the day")

    class Meta:
        unique_together = ('therapist', 'date')

    def __str__(self):
        return f"{self.therapist.name} - {self.date}"

    def get_available_slots(self):
        if isinstance(self.available_slots, list):
            return [slot for slot in self.available_slots if slot.get("status") == "available"]
        return []
