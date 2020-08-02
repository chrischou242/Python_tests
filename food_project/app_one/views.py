from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import *

def index(request):
    return render(request,'index.html')

def log_out(request):
    request.session.flush()
    return redirect ('/')
    
def register_account(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        
        for key, value in errors.items():
            messages.error(request, value)
       
        return redirect('/')
    else:
        new_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        freshly_created_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password =new_password

            )
        request.session['uid'] = freshly_created_user.id
        
        return redirect('/stores')

def login_account(request):
    errors = User.objects.login_validator(request.POST)
    
    if len(errors) > 0:
       
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:  
        user_with_matching_email = User.objects.filter(
            email=request.POST['email']).first()
        request.session['uid'] = user_with_matching_email.id
        request.session['email'] = user_with_matching_email.email
        request.session['first_name'] = user_with_matching_email.first_name
        request.session['last_name'] = user_with_matching_email.last_name
        
        return redirect('/stores')

def stores(request):
    if not "uid" in request.session:
        return redirect('/')
    if request.method =='POST':
        errors =Restaurant.objects.food_validator(request.POST)
        if len(errors)>0:

            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/stores')
        else:  
            new_store = Restaurant.objects.create(
                store_name = request.POST['store_name'],
                foods_sold = request.POST['foods_sold'],
                cuisine = request.POST['cuisine'],
                user = User.objects.get(id=request.session['uid'])
            )
        return redirect('/stores')
    context ={
        "user" : User.objects.get(id=request.session['uid']),
        'stores' : Restaurant.objects.all()
        }
    return render(request,'all_stores.html',context)

def join(request,stores_id):
    if not "uid" in request.session:
        return redirect('/')
    context ={
        "user" : User.objects.get(id=request.session['uid']),
        'stores' : Restaurant.objects.get(id=stores_id)
    }
    return render(request,'view_store.html',context)



def eat(request,stores_id):
    if not "uid" in request.session:
        return redirect('/')
    user_id = User.objects.get(id=request.session['uid'])
    eat = Restaurant.objects.get(id=stores_id)
    user_id.visits.add(eat)
    return redirect('/join/'+str(stores_id))

def leave(request, stores_id):
    if not "uid" in request.session:
        return redirect('/')
    user_id = User.objects.get(id=request.session['uid'])
    eat = Restaurant.objects.get(id=stores_id)
    user_id.visits.remove(eat)
    return redirect('/join/'+str(stores_id))

def close(request, stores_id):
    if not "uid" in request.session:
        return redirect('/')
    close_store = Restaurant.objects.get(id=stores_id)
    if request.session['uid'] == close_store.user.id:
        close_store.delete()
    return redirect('/stores')
