from django.urls import path
from .views      import SignUpView, SigninView, Example

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SigninView.as_view()),
]
