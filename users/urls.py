from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard, register, edit, logout_view, change_password, password_change_done

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    # change password
    path('password_change/', change_password, name='password_change'),
    path('password_change_done/', password_change_done, name='password_change_done'),
   

    # Reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        success_url='/account/password_reset_done'
    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/account/reset/done'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('', dashboard, name='dashboard'),

]

