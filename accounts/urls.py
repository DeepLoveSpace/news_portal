from django.urls import path
from .views import SignUp, ProfileUpdateView, UpgradeToAuthor

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('upgrade/', UpgradeToAuthor.as_view(), name='upgrade_to_author'),
]