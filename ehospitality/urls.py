from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from core.views import PatientLoginView, StaffLoginView, home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient/login/', PatientLoginView.as_view(), name='patient_login'),
    path('staff/login/', StaffLoginView.as_view(), name='staff_login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('core/', include('core.urls')),
    path('', home, name='home'),
]
