from django.contrib import messages
from django.shortcuts import redirect, render

import bcrypt

from .models import *

# Create your views here.

# Render Templates


def index(request):
    return render(request, 'index.html')


def view_all_books(request):
    # if we don't have a user in session
    if 'user_id' not in request.session:
        # redirect them
        return redirect('/')
    context = {
        'all_reviews': Review.objects.all().order_by('created_at')[0:3],
        'all_books': Book.objects.all()
    }
    return render(request, 'books.html', context)


def view_user(request, user_id):
    # if we don't have a user in session
    if 'user_id' not in request.session:
        # redirect them
        return redirect('/')
    print(user_id)
    context = {
        'entire_logged_in_user_object': User.objects.get(id=user_id)
    }
    return render(request, 'user.html', context)


def view_book(request, book_id):
    # if we don't have a user in session
    if 'user_id' not in request.session:
        # redirect them
        return redirect('/')
    print(book_id)
    context = {
        'book': Book.objects.get(id=book_id)
    }
    return render(request, 'book.html', context)


def view_add_book_form(request):
    # if we don't have a user in session
    if 'user_id' not in request.session:
        # redirect them
        return redirect('/')
    context = {
        'all_authors': Author.objects.all()
    }
    return render(request, 'add_book.html', context)


# Redirect routes

def logout_session(request):
    request.session.flush()
    return redirect('/')


def register(request):
    print(request.POST)
    # run validations
    errors = User.objects.register_validator(request.POST)
    print(errors)
    # generate errors
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        print('we made it in the if block so we have errors')
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, key)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        # hash the password
        print(request.POST['password'])
        hash_browns = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print('hash_browns: ', hash_browns)
        # create a user
        new_user = User.objects.create(
            name=request.POST['name'],
            alias=request.POST['alias'],
            email=request.POST['email'],
            password=hash_browns,
        )
        # start session
        request.session['user_id'] = new_user.id
        request.session['username'] = new_user.alias
        print('*'*50)
        print(new_user.password)
        return redirect('/books')


def login_user(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:  # check again
        user_with_matching_email = User.objects.filter(
            email=request.POST['login_email']).first()
        request.session['user_id'] = user_with_matching_email.id
        request.session['username'] = user_with_matching_email.alias
        return redirect('/books')


def create_a_book(request):
    print(request.POST)
    # create a book
    newly_created_book = Book.objects.create(
        book_title=request.POST['book_title']
    )

    # check if we need a new author
    if request.POST['new_author'] != '':
        print('we need a new author')
        # create a new author
        new_author = Author.objects.create(
            full_name=request.POST['new_author'])
        # associate it with the book
        newly_created_book.authors.add(new_author)
        # we only need to add it one way
        # new_author.all_books.add(newly_created_book)
    else:
        # use existing author
        print('we will use an existing author')
        # get existing author instance from db
        matching_author = Author.objects.get(
            id=request.POST['existing_author_id'])
        newly_created_book.authors.add(matching_author)

    # always
    # create a review
    Review.objects.create(
        rating=request.POST['review_rating'],
        text=request.POST['review_text'],
        user_who_wrote_this=User.objects.get(id=request.session['user_id']),
        book=newly_created_book
    )

    return redirect('/books/' + str(newly_created_book.id))


def create_review(request):
    print(request.POST)
    # create a review
    Review.objects.create(
        rating=request.POST['review_rating'],
        text=request.POST['review_text'],
        user_who_wrote_this=User.objects.get(id=request.session['user_id']),
        book=Book.objects.get(id=request.POST['book_id'])
    )
    return redirect('/books/' + str(request.POST['book_id']))


def book_remove(request, book_id):
    to_delete = Book.objects.get(id=book_id)
    to_delete.delete()
    return redirect('/books')
