from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .filters import OrderFilter

from .models import Order, Category
from .forms import SignUpForm, NewOrderForm
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def profile(request):
    context = {

    }
    return render(request, 'profile.html', context=context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def index(request):
    context = {

    }
    return render(request, 'index.html', context=context)


@login_required
def ordercreate(request):
    if request.method == 'POST':
        form = NewOrderForm(request.POST, request.FILES)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.orderer = request.user
            stock.status = 'н'
            stock.category = stock.category
            stock.save()
            form.save_m2m()
            return redirect('myorders')
    else:
        form = NewOrderForm()
    return render(request, 'order_form.html', {'form': form})


class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(orderer=self.request.user).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs, )
        context['filter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
        return context


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'


class OrderDeleteView(generic.DeleteView):
    model = Order
    success_url = reverse_lazy('myorders')
    template_name = 'delete_confirm.html'

    def get_object(self, queryset=None):
        """
        Check the logged in user is the owner of the object or 404
        """
        obj = super(OrderDeleteView, self).get_object(queryset)
        if obj.orderer != self.request.user:
            raise Http404(
                "You don't own this object"
            )
        return obj

# class DeleteCar(DeleteView):
#     model = Car
#     success_url = reverse_lazy('c2crental:list_user_cars')
#     template_name = 'c2crental/car/delete_confirm_car.html'
#     success_message = _("Car has been deleted.")
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super(DeleteCar, self).delete(request, *args, **kwargs)
#
#     def get_queryset(self):
#         owner = self.request.user
#         return self.model.objects.filter(owner=owner)
#
#     def get_object(self, queryset=None):
#         """
#         Check the logged in user is the owner of the object or 404
#         """
#         obj = super(MyView, self).get_object(queryset)
#         if obj.owner != self.request.user:
#             raise Http404(
#                 _("You don't own this object")
#             )
#         return obj
