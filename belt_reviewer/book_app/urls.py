from django.urls import path

from . import views

urlpatterns = [
    # Rendering Routes
    path('', views.index),
    path('books', views.view_all_books),
    path('users/<int:user_id>', views.view_user),
    path('books/<int:book_id>', views.view_book),
    path('books/add', views.view_add_book_form),


    # Processing Route
    path('logout', views.logout_session),
    path('register', views.register),
    path('login', views.login_user),
    path('books/create', views.create_a_book),
    path('reviews/create', views.create_review),
    path('books/remove/<int:book_id>', views.book_remove),

]
