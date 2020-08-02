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
        
        return redirect('/trips')

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
        
        return redirect('/trips')



def my_trips(request):
    if not "uid" in request.session:
        return redirect('/')
    if request.method=='POST':
        errors = Plan.objects.trip_validator(request.POST)
    
        if len(errors) > 0:
       
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/trips/create')
        else:  
            create_trip = Plan.objects.create(
                destination = request.POST['destination'],
                start_date = request.POST['start_date'],
                end_date = request.POST['end_date'],
                plan = request.POST['plan'],
                users = User.objects.get(id=request.session['uid'])
            )
          
        return redirect('/trips')
    context ={
        "user" : User.objects.get(id=request.session['uid']),
       
        }
    return render(request,'trips.html',context)

def create_trip(request):
    if not "uid" in request.session:
        return redirect('/')
    context ={
        "user" : User.objects.get(id=request.session['uid']),
       
        }
    return render(request,'create_trip.html',context)

def edit_trip(request,trip_id):
    if not "uid" in request.session:
        return redirect('/')
    if request.method=='POST':
        errors = Plan.objects.trip_validator(request.POST)
    
        if len(errors) > 0:
       
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit/'+str(trip_id)+'/trip')
        else:  
            edit_trip = Plan.objects.get(id=trip_id)
            edit_trip.destination = request.POST['destination']
            edit_trip.start_date = request.POST['start_date']
            edit_trip.end_date=request.POST['end_date']
            edit_trip.plan = request.POST['plan']
            edit_trip.save()
            return redirect('/trips')
    context ={
        "user" : User.objects.get(id=request.session['uid']),
        'trip' :Plan.objects.get(id=trip_id)
    }
    context['start_date'] =context['trip'].start_date.strftime("%Y-%m-%d")
    return render(request,'edit_trip.html',context)

def remove_trip(request, trip_id):
    if not "uid" in request.session:
        return redirect('/')
    remove_trips= Plan.objects.get(id=trip_id)
    if request.session['uid']==remove_trips.users.id:
        remove_trips.delete()
    return redirect('/trips')