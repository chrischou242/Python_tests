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
        
        return redirect('/wishes')

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
        
        return redirect('/wishes')

def my_wishes(request):
    if not "uid" in request.session:
        return redirect('/')
    if request.method=='POST':
        errors = User.objects.wish_validator(request.POST)
    
        if len(errors) > 0:
       
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/create')
        else:  
            create_wish = Wish.objects.create(
                item = request.POST['item'],
                description = request.POST['description'],
                users = User.objects.get(id=request.session['uid'])
            )
          
        return redirect('/wishes')
    context ={
        "user" : User.objects.get(id=request.session['uid']),
        
        }
    return render(request,'wishes.html',context)

def wishes_create(request):
    if not "uid" in request.session:
        return redirect('/')
    context ={
        "user" : User.objects.get(id=request.session['uid']),
       
        }
    return render(request,'create_wish.html',context)

def wishes_edit(request,wish_id):
    if not "uid" in request.session:
        return redirect('/')
    if request.method=='POST':
        errors = Wish.objects.wish_validator(request.POST)
    
        if len(errors) > 0:
       
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit/'+str(wish_id)+'/wish')
    
        create_new_edit = Wish.objects.get(id=wish_id)
        create_new_edit.item = request.POST['item']
        create_new_edit.description=request.POST['description']
        create_new_edit.save()
        return redirect('/wishes')

    context = {
        "user" : User.objects.get(id=request.session['uid']),
        "wish" : Wish.objects.get(id=wish_id)
    }

    return render(request,'edit_wish.html',context)

def wishes_remove(request, wish_id):
    if not "uid" in request.session:
        return redirect('/')
    remove_wish = Wish.objects.get(id=wish_id)
    remove_wish.delete()
    return redirect('/wishes')