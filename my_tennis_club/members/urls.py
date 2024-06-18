from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, CustomUserViewSet, GetCsrfToken, LoginViewSet

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="user")
router.register(r"register", UserRegistrationViewSet, basename="register")
urlpatterns = [
    path('', include(router.urls)),
    path('get-csrf-token/', GetCsrfToken, name="get-csrf-token"),
    path('login/', LoginViewSet.as_view(), name="login")
]