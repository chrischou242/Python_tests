from django.urls import path
from.import views
urlpatterns = [
    
    # page 1 login/registration/logout/cancel
    path('',views.index),
    path('register',views.register_account),
    path('login', views.login_account),
    path('logout',views.log_out),
    

    # page 2
    path('wishes',views.my_wishes),
    path('wishes/create', views.wishes_create),
    path('edit/<int:wish_id>/wish',views.wishes_edit),
    path('remove/<int:wish_id>/wish',views.wishes_remove)
]