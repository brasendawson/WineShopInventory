from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Drink, EditHistory
from rest_framework.views import APIView
# from .serializers import DrinkSerializer
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
from wineshop.settings import LOW_QUANTITY
from django.contrib import messages



def home(request):
    return render(request, 'home.html')



class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        drinks = Drink.objects.filter().order_by('id')

        low_drinks = Drink.objects.filter(
			employee=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		)

        if low_drinks.count() > 0:
            if low_drinks.count() > 1:
                messages.error(request, f'{low_drinks.count()} drinks have low stock')
            else:
                messages.error(request, f'{low_drinks.count()} drink has low stock')

        low_drinks_ids = Drink.objects.filter(
			employee=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		).values_list('id', flat=True)

        return render(request, 'dashboard.html', {'drinks': drinks, 'low_drinks_ids': low_drinks_ids})



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



# class DrinkListCreateView(generics.ListCreateAPIView):
#     queryset = Drink.objects.all()
#     serializer_class = DrinkSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
#     search_fields = ['name', 'category', 'quantity']
#     ordering_fields = ['quantity', 'price']
#     filterset_fields = ['category']

#     def perform_create(self, serializer):
#         serializer.save(employee=self.request.user)
        





# class DrinkDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Drink.objects.all()
#     serializer_class = DrinkSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

#     def perform_update(self, serializer):
#         if self.get_object().employee != self.request.user:
#             raise permissions.PermissionDenied("You cannot edit someone else's Inventory.")
#         serializer.save()

#     def perform_destroy(self, instance):
#         if instance.employee != self.request.user:
#             raise permissions.PermissionDenied("You cannot delete someone else's Inventory.")
#         instance.delete()



# class DrinkByTypeView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, category):
#         drinks = Drink.objects.filter(category__icontains=category)
#         serializer = DrinkSerializer(drinks, many=True)
#         return Response(serializer.data)

# Create your views here.



class AddDrink(LoginRequiredMixin, CreateView):
	model = Drink
	form_class = DrinkForm
	template_name = 'item_form.html'
	success_url = reverse_lazy('dashboard')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

	def form_valid(self, form):
		form.instance.employee = self.request.user
		return super().form_valid(form)

class EditDrink(LoginRequiredMixin, UpdateView):
    model = Drink
    form_class = DrinkForm
    template_name = 'item_form_edit.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.employee = self.request.user
        response = super().form_valid(form)
        # Create an EditHistory entry
        EditHistory.objects.create(drink=self.object, editor=self.request.user)
        return response


class DeleteDrink(LoginRequiredMixin, DeleteView):
	model = Drink
	template_name = 'delete_drink.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'