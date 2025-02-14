from django.contrib.auth import views as auth_views
from django.urls import path
from .views import DrinkListCreateView, DrinkDetailView, DrinkByTypeView, Dashboard, SignUpView
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-drink/', DrinkListCreateView.as_view(), name='add-drink'),
    path('signup/', SignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',
        auth_views.LogoutView.as_view(template_name='logout.html'),
        name='logout'),
    path('drinks/', DrinkListCreateView.as_view(), name='drink-list'),
    path('drinks/<int:pk>/', DrinkDetailView.as_view(), name='drink-detail'),
    path('drinks/category/<str:category>/', DrinkByTypeView.as_view(), name='drink-by-category'),
]