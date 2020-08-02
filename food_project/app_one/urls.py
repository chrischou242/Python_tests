from django.urls import path
from.import views
urlpatterns = [
    
    # page 1 login/registration/logout/cancel
    path('',views.index),
    path('register',views.register_account),
    path('login', views.login_account),
    path('logout',views.log_out),


    path('stores',views.stores),
    path('join/<int:stores_id>', views.join),
    
    
    path('joins/<int:stores_id>',views.eat),
    path('leave/<int:stores_id>',views.leave),
    path('close/<int:stores_id>',views.close),
    

]