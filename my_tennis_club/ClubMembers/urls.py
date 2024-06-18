from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClubViewSet, ClubMemberViewSet

router = DefaultRouter()

router.register(r"manage-club", ClubViewSet, basename="club")
router.register(r"manage-user", ClubMemberViewSet, basename="club-member")
urlpatterns = [
    path('', include(router.urls)),
]