import random
import os
import io
import zipfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import make_aware
from django.db.models import Sum
from django.http import HttpResponse
from datetime import datetime, timedelta
from .models import CustomerUser, Bus, Route, Trip, Booking
from .forms import BusForm, RouteForm, TripForm

# Dynamic Database Seeding
def seed_data_if_empty():
    if Bus.objects.exists() or Route.objects.exists():
        return

    # 1. Create Default Users
    staff_user = CustomerUser.objects.create(
        email='admin@nts.ug',
        full_name='Admin Staff (NTS)',
        phone='+256 701 234567',
        role='staff',
        password='admin'
    )
    customer_user = CustomerUser.objects.create(
        email='customer@nts.ug',
        full_name='Nahate Simon',
        phone='+256 772 987654',
        role='customer',
        password='password'
    )

    # 2. Seed Buses
    buses = [
        Bus.objects.create(name='NTS Link Express', plate_number='UAY 421B', capacity=44, type='VIP'),
        Bus.objects.create(name='YY Coaches', plate_number='UBD 109F', capacity=48, type='Classic'),
        Bus.objects.create(name='Gaaga Royal', plate_number='UBA 567H', capacity=40, type='Executive'),
        Bus.objects.create(name='Nile Star Coach', plate_number='UBC 888X', capacity=44, type='Executive'),
        Bus.objects.create(name='Horizon Coaches', plate_number='UAX 912K', capacity=48, type='Classic'),
    ]

    # 3. Seed Routes
    routes = [
        Route.objects.create(departure='Kampala', destination='Jinja', distance='80 km', estimated_time='2h 00m'),
        Route.objects.create(departure='Jinja', destination='Mukono', distance='55 km', estimated_time='1h 15m'),
        Route.objects.create(departure='Jinja', destination='Kampala', distance='80 km', estimated_time='2h 00m'),
        Route.objects.create(departure='Mbale', destination='Soroti', distance='105 km', estimated_time='2h 15m'),
        Route.objects.create(departure='Kampala', destination='Gulu', distance='335 km', estimated_time='5h 30m'),
        Route.objects.create(departure='Kampala', destination='Mbarara', distance='270 km', estimated_time='4h 00m'),
        Route.objects.create(departure='Kampala', destination='Mbale', distance='225 km', estimated_time='4h 30m'),
    ]

    # Helper for dates relative to now
    now = datetime.now()

    # 4. Seed Trips
    trips_data = [
        {'route_idx': 0, 'bus_idx': 0, 'hours': 2, 'fare': 25000},
        {'route_idx': 1, 'bus_idx': 4, 'hours': 3.5, 'fare': 15000},
        {'route_idx': 2, 'bus_idx': 2, 'hours': 5, 'fare': 20000},
        {'route_idx': 3, 'bus_idx': 1, 'hours': 1.5, 'fare': 22000},
        {'route_idx': 4, 'bus_idx': 3, 'hours': 6, 'fare': 45000},
        {'route_idx': 5, 'bus_idx': 0, 'hours': 8, 'fare': 35000},
        {'route_idx': 6, 'bus_idx': 1, 'hours': 4, 'fare': 30000},
    ]

    for data in trips_data:
        dep_time = now + timedelta(hours=data['hours'])
        arr_time = dep_time + timedelta(hours=2) # default 2h trip duration
        t = Trip.objects.create(
            route=routes[data['route_idx']],
            bus=buses[data['bus_idx']],
            departure_time=make_aware(dep_time),
            arrival_time=make_aware(arr_time),
            fare=data['fare'],
            status='Scheduled'
        )
        
        # Pre-seed some random bookings for realism
        seats_reserved = sorted([random.randint(1, 20) for _ in range(random.randint(1, 5))])
        if seats_reserved:
            selected_seats_str = ",".join(map(str, seats_reserved))
            total_cost = len(seats_reserved) * t.fare
            ref_num = f"NTS-UG-{random.randint(1000, 9999)}"
            Booking.objects.create(
                trip=t,
                user=customer_user,
                passenger_name=customer_user.full_name,
                passenger_phone=customer_user.phone,
                selected_seats=selected_seats_str,
                total_amount=total_cost,
                payment_method='mtn_momo',
                payment_status='Paid',
                booking_ref=ref_num,
                status='Confirmed'
            )

# Primary views
def trips_view(request):
    seed_data_if_empty()
    
    # Query distinct cities for search filters
    departures_cities = sorted(list(set(Route.objects.values_list('departure', flat=True))))
    destinations_cities = sorted(list(set(Route.objects.values_list('destination', flat=True))))

    selected_departure = request.GET.get('searchDeparture', '')
    selected_destination = request.GET.get('searchDestination', '')
    selected_class = request.GET.get('classFilter', 'All')

    # Start with all scheduled or boarding trips
    trips_query = Trip.objects.filter(status__in=['Scheduled', 'Boarding']).order_by('departure_time')

    if selected_departure:
        trips_query = trips_query.filter(route__departure__iexact=selected_departure)
    if selected_destination:
        trips_query = trips_query.filter(route__destination__iexact=selected_destination)
    if selected_class and selected_class != 'All':
        trips_query = trips_query.filter(bus__type=selected_class)

    # Context values
    trips_list = []
    for t in trips_query:
        trips_list.append({
            'trip': t,
            'reserved_seats': t.reserved_seats_list(),
            'seats_left': t.seats_left()
        })

    # Seat Selection Highlight
    reserving_trip_id = request.GET.get('trip_id')
    reserving_trip = None
    reserving_trip_seats = []
    reserving_trip_reserved = []
    if reserving_trip_id:
        try:
            reserving_trip = Trip.objects.get(id=reserving_trip_id)
            reserving_trip_reserved = reserving_trip.reserved_seats_list()
            # Generate capacity range for seats 1-indexed
            reserving_trip_seats = range(1, reserving_trip.bus.capacity + 1)
        except Trip.DoesNotExist:
            pass

    context = {
        'trips': trips_list,
        'departures': departures_cities,
        'destinations': destinations_cities,
        'selected_departure': selected_departure,
        'selected_destination': selected_destination,
        'selected_class': selected_class,
        'reserving_trip': reserving_trip,
        'reserving_trip_seats': reserving_trip_seats,
        'reserving_trip_reserved': reserving_trip_reserved,
    }
    return render(request, 'trips.html', context)


def book_trip_view(request):
    if request.method != 'POST':
        return redirect('trips')

    trip_id = request.POST.get('trip_id')
    trip = get_object_or_404(Trip, id=trip_id)

    passenger_name = request.POST.get('passenger_name')
    passenger_phone = request.POST.get('passenger_phone')
    selected_seats_str = request.POST.get('selected_seats_str', '') # CSV: "1,2,3"
    payment_method = request.POST.get('payment_method', 'mtn_momo')

    if not selected_seats_str:
        messages.error(request, "Please select at least one seat to book!")
        return redirect(f"/?trip_id={trip_id}")

    # Compute amount due
    seat_indices = [int(s.strip()) for s in selected_seats_str.split(',') if s.strip().isdigit()]
    count_seats = len(seat_indices)
    
    # Calculate premium pricing (seats 1-8 are VIP front row seats, cost extra 5,000 UGX premium)
    total_cost = 0
    for s in seat_indices:
        premium = 5000 if s <= 8 else 0
        total_cost += (trip.fare + premium)

    # Double-check seat occupancy before creating booking
    current_reserved = trip.reserved_seats_list()
    for s in seat_indices:
        if s in current_reserved:
            messages.error(request, f"Seat {s} fell occupied just now. Please select another seat!")
            return redirect(f"/?trip_id={trip_id}")

    # Create the Booking Record
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = CustomerUser.objects.get(id=user_id)
        except CustomerUser.DoesNotExist:
            pass

    booking_ref = f"NTS-UG-{random.randint(1001, 9999)}"

    booking = Booking.objects.create(
        trip=trip,
        user=user,
        passenger_name=passenger_name,
        passenger_phone=passenger_phone,
        selected_seats=selected_seats_str,
        total_amount=total_cost,
        payment_method=payment_method,
        payment_status='Paid', # Automated mobile payment simulation completes instantly
        booking_ref=booking_ref,
        status='Confirmed'
    )

    messages.success(request, f"Booking completed successfully! Reference: {booking_ref}")
    return redirect('history')


def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Restrict to booking owner or staff
    user_id = request.session.get('user_id')
    current_user = None
    if user_id:
        current_user = get_object_or_404(CustomerUser, id=user_id)

    if not current_user or (current_user.role != 'staff' and booking.user != current_user):
        messages.error(request, "You are not authorized to cancel this booking.")
        return redirect('history')

    booking.status = 'Cancelled'
    booking.save()
    messages.success(request, f"Booking {booking.booking_ref} cancelled successfully.")
    
    if current_user.role == 'staff':
        return redirect('staff')
    return redirect('history')


# Authentication Views
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        try:
            user = CustomerUser.objects.get(email__iexact=email, password=password)
            request.session['user_id'] = user.id
            messages.success(request, f"Welcome back, {user.full_name}!")
            # Redirect appropriately based on role
            if user.role == 'staff':
                return redirect('staff')
            return redirect('trips')
        except CustomerUser.DoesNotExist:
            messages.error(request, "Invalid email or password. Please try again.")

    return redirect('trips')


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'customer')

        if CustomerUser.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('trips')

        user = CustomerUser.objects.create(
            email=email,
            full_name=full_name,
            phone=phone,
            password=password,
            role=role
        )
        request.session['user_id'] = user.id
        messages.success(request, f"Account created! Welcome, {full_name}!")
        if user.role == 'staff':
            return redirect('staff')
        return redirect('trips')

    return redirect('trips')


def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('trips')


def history_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.info(request, "Please sign in to view your ticketing vouchers.")
        return redirect('trips')

    user = get_object_or_404(CustomerUser, id=user_id)
    user_bookings = Booking.objects.filter(user=user).order_by('-booking_date')

    context = {
        'bookings': user_bookings,
        'view_user': user,
    }
    return render(request, 'history.html', context)


# Staff Area & Admin Dashboard
def staff_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Access restricted! Staff login required.")
        return redirect('trips')

    current_user = get_object_or_404(CustomerUser, id=user_id)
    if current_user.role != 'staff':
        messages.error(request, "Staff clearance is required to view operations panel.")
        return redirect('trips')

    # CRUD Lists
    buses = Bus.objects.all()
    routes = Route.objects.all()
    trips = Trip.objects.all().order_by('departure_time')
    bookings = Booking.objects.all().order_by('-booking_date')

    # Analytical figures
    total_revenue = Booking.objects.filter(payment_status='Paid', status='Confirmed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Tabs configuration
    active_tab = request.GET.get('tab', 'overview')

    # Addition Forms
    bus_form = BusForm()
    route_form = RouteForm()
    trip_form = TripForm()

    context = {
        'buses': buses,
        'routes': routes,
        'trips': trips,
        'bookings': bookings,
        'total_revenue': total_revenue,
        'active_tab': active_tab,
        'bus_form': bus_form,
        'route_form': route_form,
        'trip_form': trip_form,
    }
    return render(request, 'staff.html', context)


def add_bus_view(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bus coach registered successfully in fleet!")
        else:
            messages.error(request, "Failed to register bus. Please check details.")
    return redirect('/staff/?tab=buses')


def add_route_view(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Travel connection route added successfully!")
        else:
            messages.error(request, "Failed to add route.")
    return redirect('/staff/?tab=routes')


def add_trip_view(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trip scheduled successfully!")
        else:
            messages.error(request, "Failed to schedule departure. Ensure all fields are valid.")
    return redirect('/staff/?tab=trips')


def download_zip_view(request):
    # This view packages the entire repository workspace on the fly (excluding local temp/binary files) and downloads it as a ZIP
    memory_file = io.BytesIO()
    
    # Absolute path of the workspace root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    ignore_dirs = {'.git', 'node_modules', '__pycache__', '.venv', '.next', 'dist'}
    ignore_files = {
        'db.sqlite3', 'get-pip.py', 'package.json', 'package-lock.json', 
        'prepare-django.js', 'start-django.js', '.env.example'
    }
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file in ignore_files or file.endswith('.pyc') or file.endswith('.pyo'):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_dir)
                zip_file.write(file_path, rel_path)
                
    memory_file.seek(0)
    response = HttpResponse(memory_file.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="nts-regional-bus-tickets-django.zip"'
    return response
