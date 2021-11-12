from django.urls import path

from .import views

urlpatterns = [
    path("/deposit", views.DepositView.as_view()),
    path("/withdrawal", views.WithdrawalView.as_view()),
]
