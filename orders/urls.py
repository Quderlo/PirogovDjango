from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders, name='orders'),
    path('search/', views.search, name='search'),
    path('clients/', views.clients, name='clients'),
    path('workers/', views.workers, name='workers'),
    path('directory/', views.directory, name='directory'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add_technique/', views.add_technique, name='add_technique'),
    path('add_client/', views.add_client, name='add_client'),
    path('add_order/', views.add_order, name='add_order'),
    path('search_order/', views.search_order, name='search_order'),
    path('view_order/<int:order_id>/', views.view_order, name='view_order'),
]