from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import request, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import UpdateView, DeleteView

from .filters import OrderFilter, AllOrderFilter

from .models import Order, Category
from .forms import SignUpForm, NewOrderForm, StatusUpdateForm, DeleteCategoryForm
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def profile(request):
    context = {}
    return render(request, 'profile.html', context=context)


def signup(request):
    """
    Обработка формы регистрации
    """
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
    """
    Главная страница
    """
    num_accepted = Order.objects.filter(status__exact='п').count()
    context = {
        'num_accepted': num_accepted
    }
    return render(request, 'index.html', context=context)


@login_required
def ordercreate(request):
    """
    Создание новой заявки
    """
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
    """
    Заявки одного пользователя с фильтром
    """
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
    """
    Детальная страница для каждого заказа
    """
    model = Order
    template_name = 'order_detail.html'


class OrderDeleteView(generic.DeleteView):
    """
    Удаление заказа
    """
    model = Order
    success_url = reverse_lazy('myorders')
    template_name = 'delete_confirm.html'

    def get_object(self, queryset=None):
        obj = super(OrderDeleteView, self).get_object(queryset)
        if obj.orderer != self.request.user:
            raise Http404(
                "Вы не автор статьи"
            )
        return obj


class AllOrdersListView(PermissionRequiredMixin, generic.ListView):
    """
    Все заявки (только для администратора)
    """
    permission_required = 'app.can_change_status'
    model = Order
    template_name = 'all_orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs, )
        context['filter'] = AllOrderFilter(self.request.GET, queryset=self.get_queryset())
        return context



@login_required
@permission_required('app.can_change_status')
def statuschange(request, pk):
    model = Order
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            order.status = form.cleaned_data['status']
            if form.cleaned_data['status'] == 'в':
                # form = CompleteStatusUpdateForm()
                return redirect('complete-order', pk)
            else:
                order.save()
            return HttpResponseRedirect(reverse('all-orders'))
    else:
        form = StatusUpdateForm()
    return render(request, 'status_form.html', {'form': form})


class CompleteStatusChange(UpdateView):
    model = Order
    fields = ['status', 'design']
    initial = {'status': 'в'}
    success_url = '/'
    template_name = 'status_form.html'


def deletecategory(request):
    if request.method == 'POST':
        form = DeleteCategoryForm(request.POST)
        if form.is_valid():
            namecat = Category.objects.get(name=form.cleaned_data['name'])
            namecat.delete()
            return HttpResponseRedirect(reverse('all-orders'))
    else:
        form = DeleteCategoryForm()
    return render(request, 'category_form.html', {'form': form})


# def completestatuschange(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     if request.method == 'POST':
#         form = CompleteStatusUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             stock = form.save(commit=False)
#             stock.status = 'в'
#             stock.save()
#             return redirect('orders')
#     else:
#         form = CompleteStatusUpdateForm()
#     return render(request, 'status_form.html', {'form': form})
