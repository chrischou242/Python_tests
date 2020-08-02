
from django.urls import path
from .import views

urlpatterns = [
    # page 1 Login
    path('',views.index),
    path('login',views.login_account),
    path('register',views.register_account),

    # page2 trip detail planner
    path('trip_planner',views.trip_detail_plan),
    path('view_new_planner',views.new_planner_trip),
    path('view_edit_trip/<int:trip_id>', views.new_edit_plan),

    # page 3 create a new trip
    path ('create_new_trip', views.create_trip),
    path('cancel',views.cancel),

    # path 4
    path('make_edit/<int:trip_id>',views.create_new_edit),
    path('remove_trip/<int:trip_id>',views. remove_trip)
]
