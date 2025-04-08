from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('budgetapp.urls')),  # Hook up your app's URLs here
]
