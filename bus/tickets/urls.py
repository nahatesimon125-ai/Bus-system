from django.urls import path
from . import views

urlpatterns = [
    path('', views.trips_view, name='trips'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/signup/', views.signup_view, name='signup'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('history/', views.history_view, name='history'),
    path('staff/', views.staff_view, name='staff'),
    path('staff/bus/add/', views.add_bus_view, name='add_bus'),
    path('staff/route/add/', views.add_route_view, name='add_route'),
    path('staff/trip/add/', views.add_trip_view, name='add_trip'),
    path('book-trip/', views.book_trip_view, name='book_trip'),
    # Extra helper endpoints
    path('cancel-booking/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('download-zip/', views.download_zip_view, name='download_zip'),
]
