from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from lognreg.models import Super_User
from .models import Super_User, Super_trip
# from time import gmtime, strftime

def index(request):
	if 'super_user' not in request.session:
		request.session['status'] = 'guest'
		return render(request, 'lognreg/lognreg.html')
	else:
		request.session['status'] = 'logged_in'
		return render(request, 'lognreg/lognreg.html', {'super_user': Super_User.objects.get(id=request.session['super_user_id'])})

def register(request):
	result = Super_User.objects.validate_registration(request.POST)
	if result['status'] != True:
		for error in result['errors']:
			messages.error(request, result['errors'][error])
		return redirect('/')
	else:
		request.session['super_user_id'] = result['super_user_id']
		return redirect ('/landing')



def login(request):
	result = Super_User.objects.validate_login(request.POST)
	if result['status'] != True:
		for error in result['errors']:
			messages.error(request, result['errors'][error])
		return redirect('/')
	else:
		request.session['super_user_id'] = result['super_user_id']
		return redirect('/landing')


def landing(request):
	if 'super_user_id' not in request.session:
		return redirect('/')
	context = {
		'trips': Super_trip.objects.exclude(joined_by= request.session["super_user_id"]),
		'joins': Super_trip.objects.filter(joined_by= request.session["super_user_id"]) 
	}
	return render(request, 'lognreg/trips.html', context)


def logout(request):
	request.session.flush()
	return redirect('/')

def trips(request):
	result = Super_trip.objects.validate_trip(request.POST, request.session)
	if result['status'] != True:
		for error in result['errors']:
			messages.error(request, result['errors'][error])
		return redirect('/landing')
	else:
		return redirect ('/landing')

def createJoinTrip(request):
		user = Super_User.objects.get(id=request.session['super_user_id'])
		trip = Super_trip.objects.get(id=request.POST['trip_id'])
		start_date = Super_trip.objects.get(id=request.POST['trip_id'])
		end_date = Super_trip.objects.get(id=request.POST['trip_id'])
		trip.joined_by.add(user)
		trip.save()
		print "request.POST"
		return redirect('/landing')

def destroyJoinTrip(request):
		user = Super_User.objects.get(id=request.session['super_user_id'])
		join = Super_trip.objects.get(id=request.POST['join_id'])
		# start_date = Super_trip.objects.get(id=request.POST['trip_id'])
		# end_date = Super_trip.objects.get(id=request.POST['trip_id'])
		join.joined_by.remove(user)
		
		print request.POST
		return redirect('/landing')





# def trip_friends(request):
	







def about_trip(request):
	if 'super_user_id' not in request.session:
		return redirect('/')
	context = {
		'trips': Super_trip.objects.exclude(joined_by= request.session["super_user_id"]),
		'joins': Super_trip.objects.filter(joined_by= request.session["super_user_id"]) 
	}
	return render(request, 'lognreg/about_trip.html', context)


# def time(request):
#   context = {
#   "time": strftime("%Y-%m-%d %H:%M %p", gmtime())
#   }
#   return render(request,'lognreg/trips.html', context)

