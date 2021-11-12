from django.urls import path, include

urlpatterns = [
    path("transactions", include("transactions.urls")),
]
