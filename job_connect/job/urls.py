from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView  # Import TemplateView
from .views import profile_overview, create_portfolio
from .views import payment_page, portfolio_list_view, forum_view, send_message, get_messages, get_online_users, post_communication, portfolio_management



urlpatterns = [
    path('', views.home, name='home'), # Root URL routed to the home view
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout, name='logout'),
    path('panel/admin/', views.admin_panel, name='admin_panel'),
    path('panel/expert/', views.expert_panel, name='expert_panel'),
    path('panel/clients/', views.clients_panel, name='clients_panel'),

    path('profile/', profile_overview, name='profile_overview'),
    path('security-settings/', views.security_settings, name='security_settings'),
    path('create-portfolio/', create_portfolio, name='create_portfolio'),
    path('portfolio-success/', TemplateView.as_view(template_name='portfolio_success.html'), name='portfolio_success'),

    path('payment/', payment_page, name='payment_page'),  # URL to access the payment page
    path('portfolios/', portfolio_list_view, name='portfolio_list'),
    path('pay-now/<str:service_type>/', views.pay_now, name='pay_now'),
    path('community/', views.community_page, name='community_page'),

    path('forum/', forum_view, name='forum'),
    path('send_message/', send_message, name='send_message'),
    path('get_messages/', get_messages, name='get_messages'),
    path('get_online_users/', get_online_users, name='get_online_users'),


    path('networking/', views.networking_form_view, name='networking_form'),
    path('job-seekers/', views.job_seeker_list_view, name='job_seeker_list'),



    path('user-management/', views.user_management, name='user_management'),
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('post-communication/', post_communication, name='post_communication'),
    path('portfolio-management/', portfolio_management, name='portfolio_management'),





]