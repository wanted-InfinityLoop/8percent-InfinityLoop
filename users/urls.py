from django.urls import path
from .views      import SignUpView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    # path('/signin', SigninView.as_view()),
    # path('/decorator-test', Example.as_view())
]
