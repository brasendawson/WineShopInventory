from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Drink
from rest_framework.views import APIView
from .serializers import DrinkSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .forms import UserRegisterForm, DrinkForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.urls import path
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Drink, Category

def home(request):
    return render(request, 'home.html')

class Dashboard(LoginRequiredMixin, View):
     def get(self, request):
         drinks = Drink.objects.filter(creator=self.request.user.id).order_by('id')

         return render(request, 'dashboard.html', {'drinks' : drinks})



class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'register.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('home')

		return render(request, 'register.html', {'form': form})



class DrinkListCreateView(generics.ListCreateAPIView):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'category', 'quantity']
    ordering_fields = ['quantity', 'price']
    filterset_fields = ['category']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)








class DrinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

    def perform_update(self, serializer):
        if self.get_object().creator != self.request.user:
            raise permissions.PermissionDenied("You cannot edit someone else's Inventory.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise permissions.PermissionDenied("You cannot delete someone else's Inventory.")
        instance.delete()

class DrinkByTypeView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, category):
        recipes = Drink.objects.filter(category__icontains=category)
        serializer = DrinkSerializer(recipes, many=True)
        return Response(serializer.data)

# Create your views here.
