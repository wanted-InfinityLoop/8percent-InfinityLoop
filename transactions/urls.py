from django.urls        import path
from .                  import views
from transactions.views import *


urlpatterns = [
    path("/deposit", views.DepositView.as_view()),
]
