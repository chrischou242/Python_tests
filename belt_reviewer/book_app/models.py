import re

from django.db import models

import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        # First Name and Last Name Check
        if len(post_data['name']) < 2:
            print("Name should be at least 2 characters")
            errors["name"] = "First Name should be at least 2 characters"
        if len(post_data['alias']) < 2:
            print("Alias should be at least 2 characters")
            errors["alias"] = "Last Name should be at least 2 characters"
        # email
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        # password
        # min length
        if len(post_data['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        # match the password confirm
        if post_data['password'] != post_data['confirm_password']:
            errors["confirm_password"] = "Password does not match"

        # validate for email uniqueness
        potential_matched_user_email_list = User.objects.filter(
            email=post_data['email'])
        if len(potential_matched_user_email_list) > 0:
            errors["email_found"] = "Email already exists"
        return errors

    # def login_validator
        # set up errors
        # check if the email is in the db - post data 'email'
        # if we did not find a user
        # generate errors
        # return redirect to login page to view errors
        # if we found a user
        # check if their password is the same
        # if it is the same
        # redirect them to the account page
        # else
        # redirect them to loging page to view errors
    def login_validator(self, post_data):
        errors = {}
        user_with_matching_email = User.objects.filter(
            email=post_data['login_email']).first()
        if user_with_matching_email == None:
            errors['login_email'] = "Not Found. Please register"
        else:  # found user and check again for password
            # password not match
            if bcrypt.checkpw(post_data['login_password'].encode(), user_with_matching_email.password.encode()) == False:
                errors['login_password'] = "Password does not Match"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    # user_reviews
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Book(models.Model):
    book_title = models.CharField(max_length=255)
    # authors
    # book_reviews
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Author(models.Model):
    full_name = models.CharField(max_length=150)
    # Many2Many added and cant use on_delete
    all_books = models.ManyToManyField(Book, related_name="authors")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    rating = models.IntegerField()
    text = models.CharField(max_length=255)
    user_who_wrote_this = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reviews")
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
