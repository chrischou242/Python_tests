from django.urls import path
from.import views
urlpatterns = [
    
    # page 1 login/registration/logout/cancel
    path('',views.index),
    path('register',views.register_account),
    path('login', views.login_account),
    path('logout',views.log_out),

    path('trips',views.my_trips),
    path('trips/create',views.create_trip),
    path('edit/<int:trip_id>/trip', views.edit_trip),
    path('remove/<int:trip_id>/trip', views.remove_trip)
    # path('remove/<int:trip_id/trip',),
]