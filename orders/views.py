# orders/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, DirectoryForm, ClientForm, OrderForm, SearchOrderForm, ProgressForm, UpdateOrderCostForm
from django.contrib.auth import authenticate, logout, login
from .models import Directory, Client, Order, Progress
from django.contrib.auth.models import User
from django.db.models import Q


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html')


def orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    all_orders = Order.objects.filter(user=request.user)

    return render(request, 'orders.html', {'orders': all_orders})


def search(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = SearchOrderForm()

    return render(request, 'search.html', {'form': form})


# orders/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = SearchOrderForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            orders = Order.objects.filter(
                Q(client__first_name__icontains=search_term) |
                Q(client__second_name__icontains=search_term) |
                Q(user__first_name__icontains=search_term) |
                Q(user__last_name__icontains=search_term)
            )

            # Добавим постраничный вывод
            page = request.GET.get('page', 1)
            paginator = Paginator(orders, 10)  # 10 элементов на странице

            try:
                orders = paginator.page(page)
            except PageNotAnInteger:
                orders = paginator.page(1)
            except EmptyPage:
                orders = paginator.page(paginator.num_pages)

            return render(request, 'search_results.html',
                          {'orders': orders, 'query': search_term, 'paginator': paginator})
    else:
        form = SearchOrderForm()

    return render(request, 'search.html', {'form': form})


def clients(request):
    if not request.user.is_authenticated:
        return redirect('login')

    all_clients = Client.objects.all()

    items_per_page = 10
    paginator = Paginator(all_clients, items_per_page)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'clients.html', {'page_obj': page_obj})


def workers(request):
    if not request.user.is_authenticated:
        return redirect('login')

    all_workers = User.objects.all()

    items_per_page = 10
    paginator = Paginator(all_workers, items_per_page)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'workers.html', {'page_obj': page_obj})


def directory(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Получение всех техник
    all_techniques = Directory.objects.all()

    # Определение количества техник на странице
    items_per_page = 10
    paginator = Paginator(all_techniques, items_per_page)

    # Получение номера текущей страницы из параметра запроса
    page_number = request.GET.get('page')
    # Если параметр не указан, используем первую страницу
    page_obj = paginator.get_page(page_number)

    return render(request, 'directory.html', {'page_obj': page_obj})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')  # Замените 'home' на вашу домашнюю страницу
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # Замените 'login' на вашу страницу входа


def add_technique(request):
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directory')  # Перенаправление на страницу со списком техники
    else:
        form = DirectoryForm()

    return render(request, 'add_technique.html', {'form': form})


def add_client(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = ClientForm()

    return render(request, 'add_client.html', {'form': form})


from .models import Order, Directory
from django.shortcuts import render, redirect
from .forms import OrderForm


def add_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            directory = form.cleaned_data['directory']
            create_new_directory = form.cleaned_data['create_new_directory']
            new_directory_name = form.cleaned_data['new_directory_name']
            new_directory_type = form.cleaned_data['new_directory_type']

            if not directory and create_new_directory and (new_directory_name and new_directory_type):
                directory = Directory.objects.create(name=new_directory_name, type=new_directory_type)

            order = form.save(commit=False)
            order.user = request.user
            order.directory = directory
            order.save()
            return redirect('orders')  # Перенаправьте на страницу с заказами после успешного создания заказа
    else:
        form = OrderForm()

    return render(request, 'add_order.html', {'form': form})


def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    progress_list = Progress.objects.filter(order=order)
    progress_form = ProgressForm()
    update_cost_form = UpdateOrderCostForm(instance=order)

    if request.method == 'POST':
        progress_form = ProgressForm(request.POST)
        if progress_form.is_valid():
            new_progress = progress_form.save(commit=False)
            new_progress.order = order
            new_progress.save()

        update_cost_form = UpdateOrderCostForm(request.POST, instance=order)
        if update_cost_form.is_valid():
            update_cost_form.save()

    return render(request, 'view_order.html',
                  {'order': order, 'progress_list': progress_list, 'progress_form': progress_form,
                   'update_cost_form': update_cost_form})
