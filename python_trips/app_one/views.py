from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
import bcrypt

def index(request):
    return render(request,'index.html')


def login_account(request):
    user_with_matching_email = User.objects.filter(email=request.POST['email'])
    if len(user_with_matching_email)>0:
        user = user_with_matching_email[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['uid']=user.id
            return redirect ('/trip_planner')
        return redirect('/')

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
        
        return redirect('/trip_planner')
    
def trip_detail_plan(request):
    if "uid" not in request.session:
        return redirect('/')
    context={
        'user' : User.objects.get(id=request.session['uid']),
        'allTrips':Trip.objects.all()
    }
    return render(request,"trip_planner.html",context)

def new_planner_trip(request):
    if "uid" not in request.session:
        return redirect('/')
    context={
        'user' : User.objects.get(id=request.session['uid'])
    }
    return render(request,'create_new_trip.html',context)

def create_trip(request):
    if "uid" not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
        
            for key, value in errors.items():
                messages.error(request, value)
       
            return redirect('/view_new_planner')
        else:
            new_trip = Trip.objects.create(
                destination = request.POST['destination'],
                plan = request.POST['plan'],
                start_date = request.POST['start_date'],
                end_date = request.POST['end_date'],
            )
            new_trip.users.add(User.objects.get(id=request.session['uid']))
        return redirect ('/trip_planner')
    else:
        return redirect('/')

def cancel(request):
    return redirect('/trip_planner')

def new_edit_plan(request, trip_id):
    if "uid" not in request.session:
        return redirect('/')
    context={
        'user' : User.objects.get(id=request.session['uid']),
        'trip':Trip.objects.get(id=trip_id)
    }
    return render (request,'create_new_edit.html',context)

def create_new_edit(request, trip_id):
    if "uid" not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/view_edit_trip/'+str(trip_id))
        edit_new_trip = Trip.objects.get(id=trip_id)
        if request.session['uid'] == edit_new_trip.users.id:
            edit_new_trip.destination = requeset.POST['destination']
            edit_new_trip.start_date=request.POST['start_date']
            edit_new_trip.end_date=request.POST['end_date']
            edit_new_trip.plan= request.POST['plan']
            edit_new_trip.save()

    return redirect('/trip_planner')
      

def remove_trip(request,trip_id):
    if "uid" not in request.session:
        return redirect('/')
    delete_trip = Trip.objects.get(id=trip_id)
    if request.session['uid'] == delete_trip.users.id:
        delete_trip.delete()
    return redirect('/trip_planner')