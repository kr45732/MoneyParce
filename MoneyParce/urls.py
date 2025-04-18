from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("overview.urls")),
    # path("", include("home.urls")),
    path("income_and_expenses", include("income_and_expenses.urls")),
    path("overview", include("overview.urls")),
    path("faqs", include("faqs.urls")),
    path("budget", include("budget.urls")),
    # path('', include('budgetapp.urls')),
]
