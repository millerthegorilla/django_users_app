from django.urls import include, path
from .views import UserLoginView, DashboardView, RegisterView, ProfileView

app_name = 'users'
urlpatterns = [
	path('accounts/login/', UserLoginView.as_view(), name='login'),
	path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile')
]