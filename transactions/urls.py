from django.urls  import path
from transactions import views

urlpatterns = [
    path("/deposit", views.DepositView.as_view()),
    path("/withdrawal", views.WithdrawalView.as_view()),
    path("/history", views.TransactionHistoryView.as_view()),
]
