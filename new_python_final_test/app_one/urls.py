from django.urls import path
from.import views
urlpatterns = [
    
    # page 1 login/registration/logout/cancel
    path('',views.index),
    path('register',views.register_account),
    path('login', views.login_account),
    path('logout',views.log_out),

    # page 2
    path('thoughts',views.my_thoughts),
    path('thoughts/<int:thought_id>', views.details),
    path('like/<int:thought_id>',views.like),
    path('delete/<int:thought_id>',views.delete),
    path('unlike/<int:thought_id>',views.unlike)
]