from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView  # Import TemplateView
from .views import profile_overview, create_portfolio
from .views import payment_page, portfolio_list_view, forum_view, send_message, get_messages, get_online_users, post_communication, portfolio_management, delete_candidate
from .views import manage_contact, reply_contact, delete_contact, forgot_password, verify_reset_code, reset_password, profile_view, profile_admin, job_applications, apply_job




urlpatterns = [
    path('', views.home, name='home'), # Root URL routed to the home view
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),


    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-reset-code/', verify_reset_code, name='verify_reset_code'),
    path('reset-password/', reset_password, name='reset_password'), 
    
    
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
    path('portfolio/delete/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),

    path('manage_contact/', manage_contact, name='manage_contact'),
    path('reply_contact/<int:contact_id>/', reply_contact, name='reply_contact'),
    path('delete_contact/<int:contact_id>/', delete_contact, name='delete_contact'),



    path('communications/', views.communication_list, name='communication_list'),
    path('communications/<int:pk>/', views.communication_detail, name='communication_detail'),
    path('communications/<int:pk>/download/', views.download_communication_pdf, name='download_communication_pdf'),
    path('experts/', views.expert_list, name='expert_list'),
    path('rate_expert/<int:expert_id>/', views.rate_expert, name='rate_expert'),
    path('experts/<int:expert_id>/comments/', views.view_comments, name='view_comments'),


    path('jobs/create/', views.create_job_post, name='create_job_post'),
    path('jobs/manage/', views.manage_jobs, name='manage_jobs'),
    path('jobs/<int:job_post_id>/applications/', views.track_applications, name='track_applications'),
    path('jobs/<int:job_id>/edit/', views.edit_job_post, name='edit_job_post'),  # Add the URL pattern for editing job posts
    path('jobs/<int:job_id>/toggle/', views.toggle_job_status, name='toggle_job_status'),
    path('jobs/manage/', views.manage_jobs, name='manage_jobs'),

    path('job-applications/', job_applications, name='job_applications'),
    path('apply-job/', apply_job, name='apply_job'),  # Adjust this as necessary
    path('analytics/', views.analytics_view, name='analytics_view'),

    


    path('messages/load/', views.load_messages, name='load_messages'),
    path('messages/send/', views.send_message, name='send_message'),
    path('messages/', views.messaging, name='messaging_page'),
    path('profile_view/', profile_view, name='profile_view'),
    path('profile_admin/', profile_admin, name='profile_admin'),
    path('setting/', views.setting, name='setting'),
    path('security/', views.security, name='security'),




    path('search/', views.candidate_search, name='candidate_search'),
    path('get_specifications/', views.get_specifications, name='get_specifications'),
    path('get_towns/', views.get_towns, name='get_towns'),
    path('get_quarters/', views.get_quarters, name='get_quarters'),
    path('search_candidates/', views.search_candidates, name='search_candidates'),
    path('candidate/<int:expert_id>/', views.candidate_details, name='candidate_details'),










]