from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Trip(models.Model):
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('trip-detail', kwargs={'pk': self.pk})

class TripNote(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.trip.title} - {self.title}"

class Photo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=200)
    image_url = models.URLField()  # Store Unsplash photo URLs
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.trip.title} - {self.title}"