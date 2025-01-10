from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from trips.views import Register, CustomPasswordResetView, CustomPasswordResetDoneView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trips.urls')),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='trips/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='trips/logout.html'), name='logout'),
    path('password-reset/', 
         CustomPasswordResetView.as_view(), 
         name='password_reset'),
    path('password-reset/done/', 
         CustomPasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='trips/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='trips/password_reset_complete.html'), 
         name='password_reset_complete'),
]