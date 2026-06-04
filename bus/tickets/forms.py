from django import forms
from .models import Bus, Route, Trip

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['name', 'plate_number', 'capacity', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
            'plate_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
            'capacity': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
            'type': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['departure', 'destination', 'distance', 'estimated_time']
        widgets = {
            'departure': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
            'destination': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
            'distance': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold', 'placeholder': 'e.g. 80 km'}),
            'estimated_time': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold', 'placeholder': 'e.g. 2h 00m'}),
        }

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['route', 'bus', 'departure_time', 'arrival_time', 'fare']
        widgets = {
            'route': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
            'bus': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold'}),
            'fare': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/20 text-xs font-semibold', 'placeholder': 'fare in UGX'}),
        }
