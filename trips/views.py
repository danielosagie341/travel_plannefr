from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Trip, TripNote, Photo
import requests
from django.conf import settings
import os
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Trip, TripNote, Photo
from .forms import UserRegisterForm
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages


class Register(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'trips/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        return render(request, 'trips/register.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'trips/password_reset.html'
    email_template_name = 'trips/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'trips/password_reset_done.html'

class TripListView(ListView):
    model = Trip
    template_name = 'trips/trip_list.html'
    context_object_name = 'trips'
    ordering = ['-created_at']
    paginate_by = 9

    def get_queryset(self):
        queryset = Trip.objects.all()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(destination__icontains=query)
            )
        return queryset

class MyTripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/my_trips.html'
    context_object_name = 'trips'
    ordering = ['-created_at']
    paginate_by = 9

    def get_queryset(self):
        queryset = Trip.objects.filter(user=self.request.user)
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(destination__icontains=query)
            )
        return queryset

class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'trips/trip_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get weather data for the destination
        weather_url = f"https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            'q': self.object.destination,
            'appid': os.getenv('OPENWEATHER_API_KEY'),
            'units': 'metric'
        }
        
        try:
            weather_response = requests.get(weather_url, params=weather_params)
            if weather_response.status_code == 200:
                context['weather'] = weather_response.json()
        except:
            context['weather'] = None

        return context

class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    template_name = 'trips/trip_form.html'
    fields = ['title', 'destination', 'start_date', 'end_date', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TripUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Trip
    template_name = 'trips/trip_form.html'
    fields = ['title', 'destination', 'start_date', 'end_date', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        trip = self.get_object()
        return self.request.user == trip.user

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this trip.")
        return redirect('trip-detail', pk=self.get_object().pk)

class TripDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Trip
    template_name = 'trips/trip_delete.html'
    success_url = reverse_lazy('trip-list')

    def test_func(self):
        trip = self.get_object()
        return self.request.user == trip.user

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete this trip.")
        return redirect('trip-detail', pk=self.get_object().pk)