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

    def wish_validator(self,postData):
        errors={}
        if len(postData['item']) < 3:
            errors["item"] = "item name should be at least 3 characters"
        
        if len(postData['description']) < 10:
            errors["description"] = "description should be at least 10 characters"
        
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects =UserManager()

class Wish(models.Model):
    item =models.CharField(max_length=255)
    description =models.CharField(max_length=255)
    users = models.ForeignKey(User, related_name='wishes', on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name="likes")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects =UserManager()