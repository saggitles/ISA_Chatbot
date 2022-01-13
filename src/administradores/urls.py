from django.urls import path
from django.contrib.auth import views as auth_views

#from django.contrib.auth.views import login, password_reset, password_reset_done, password_reser_confirm, password_reset_complete
#from .views import AdministradoresLoginView
urlpatterns = [
    path('reset_password/', auth_views.PasswordResetView.as_view( template_name='registration/password_reset.html'),name='password_reset'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view( template_name='registration/password_done.html'),name= "password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetView.as_view( template_name='registration/password_confirm.html'),name ="password_reset_confirm" ),
    path('reset_password_complete/',auth_views.PasswordResetView.as_view( template_name='registration/password_complete.html'),name= "password_reset_complete"),
]
