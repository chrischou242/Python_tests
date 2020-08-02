from django.db import models
import re

class UserManger(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 4:
            errors["first_name"] = "Password name should be at least 5 characters"
        
        if len(postData['last_name']) < 4:
            errors["last_name"] = "last name should be at least 5 characters"
        
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"

        if len(postData['password']) < 5:
            errors["password"] = "password description should be at least 10 characters"
       
        elif postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Password does not match"

        return errors



class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        
        if len(postData['plan'])<3:
            errors['plan'] = "plan should be atleast 3 characters long"

        if len(postData['destination']) < 3:
            errors["destination"] = "destination should be at least 3 characters"
    
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects =UserManger()


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    plan= models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name="personal_trips", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name= "trips")
    start_date = models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TripManager()