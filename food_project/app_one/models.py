
import re
from django.db import models
import bcrypt
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
       
        if len(postData['first_name']) < 4:
            errors["first_name"] = "Password name should be at least 4 characters"
        
        if len(postData['last_name']) < 4:
            errors["last_name"] = "last name should be at least 4 characters"
        
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
     
       
        if len(postData['password']) < 5:
            errors["password"] = "password description should be at least 5 characters"
       
        elif postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Password does not match"
     
        potential_matched_user_email_list = User.objects.filter(
        email=postData['email'])
        if len(potential_matched_user_email_list) > 0:
            errors["email_found"] = "Email already exists"
        return errors

    def login_validator(self, postData):
        errors = {}
        user_with_matching_email = User.objects.filter(
            email=postData['email']).first()
        if user_with_matching_email == None:
            errors['email'] = "Not Found. Please register"
        else:  
            if bcrypt.checkpw(postData['password'].encode(), user_with_matching_email.password.encode()) == False:
                errors['password'] = "Password does not Match"
        return errors

class FoodManager(models.Manager):
    def food_validator(self,postData):
        errors = {}
        if len(postData['foods_sold']) < 4:
            errors["foods_sold"] = "Food name should be at least 4 characters"
        
        if len(postData['store_name']) < 2:
            errors["store_name"] = "Restaurant name should be at least 4 characters"

        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects =UserManager()


class Restaurant(models.Model):
    store_name = models.CharField(max_length=255)
    foods_sold = models.CharField(max_length=255)
    cuisine = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='restaruants', on_delete = models.CASCADE)
    users = models.ManyToManyField(User, related_name='visits')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects =FoodManager()
    
    
   