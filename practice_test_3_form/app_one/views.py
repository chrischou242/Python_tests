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
        
        return redirect('/forms')

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
        
        return redirect('/forms')

def all_forms(request):
    if not "uid" in request.session:
        return redirect('/')
    if request.method=='POST':
        errors = Quote.objects.quote_validator(request.POST)
    
        if len(errors) > 0:
       
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/forms')
        else:  
            new_form = Quote.objects.create(
                author =request.POST['author'],
                quote = request.POST['quote'],
                users = User.objects.get(id=request.session['uid'])
            )
            return redirect('/forms')
    context ={
        "user" : User.objects.get(id=request.session['uid']),
        
        }
    return render(request,'form.html',context)
