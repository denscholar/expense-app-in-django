from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('expensesAPP.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path("authentication/", include('authentication.urls')),
]
