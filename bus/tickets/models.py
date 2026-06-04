from django.db import models

class CustomerUser(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    ]
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    password = models.CharField(max_length=100) # Simple storage matching earlier demo state

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class Bus(models.Model):
    TYPE_CHOICES = [
        ('Classic', 'Classic'),
        ('Executive', 'Executive'),
        ('VIP', 'VIP'),
    ]
    name = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=50, unique=True)
    capacity = models.IntegerField(default=40)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Classic')

    def __str__(self):
        return f"{self.name} [{self.plate_number}]"

class Route(models.Model):
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.CharField(max_length=50) # e.g. "80 km"
    estimated_time = models.CharField(max_length=50) # e.g. "2h 00m"

    def __str__(self):
        return f"{self.departure} ➜ {self.destination} ({self.distance})"

class Trip(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Boarding', 'Boarding'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trips')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='trips')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    fare = models.IntegerField() # in UGX
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Scheduled')

    def reserved_seats_list(self):
        # Query active bookinigs to find reserved seats
        bookings = self.bookings.filter(status='Confirmed')
        reserved = []
        for b in bookings:
            if b.selected_seats:
                for seat_str in b.selected_seats.split(','):
                    seat_str = seat_str.strip()
                    if seat_str:
                        try:
                            reserved.append(int(seat_str))
                        except ValueError:
                            pass
        return sorted(list(set(reserved)))

    def seats_left(self):
        return self.bus.capacity - len(self.reserved_seats_list())

    def __str__(self):
        return f"{self.route} via {self.bus.name} at {self.departure_time}"

class Booking(models.Model):
    PAY_METHOD_CHOICES = [
        ('mtn_momo', 'MTN MoMo'),
        ('airtel_money', 'Airtel Money'),
        ('card', 'Credit/Debit Card'),
    ]
    PAY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(CustomerUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    passenger_name = models.CharField(max_length=150)
    passenger_phone = models.CharField(max_length=50)
    selected_seats = models.CharField(max_length=200) # e.g. "5,6,12"
    total_amount = models.IntegerField() # total cost paid (in UGX)
    payment_method = models.CharField(max_length=50, choices=PAY_METHOD_CHOICES)
    payment_status = models.CharField(max_length=30, choices=PAY_STATUS_CHOICES, default='Pending')
    booking_ref = models.CharField(max_length=50, unique=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Confirmed')

    def seats_list(self):
        if not self.selected_seats:
            return []
        return [int(s.strip()) for s in self.selected_seats.split(',') if s.strip().isdigit()]

    def __str__(self):
        return f"{self.booking_ref} - {self.passenger_name} ({self.status})"
