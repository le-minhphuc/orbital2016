from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json
# Create your views here.
from .models import MugSpot, Person, Position, LiveUpdate
from .forms import UserRegisterForm, UserLoginForm

def index(request, place_id=0):
	def find_pos(usr):
		place_indicator = True
		user_pos = Position.objects.filter(user=usr)
		if len(user_pos) == 0:
			return "No position object yet"
		user_pos = user_pos[0]
		all_places = MugSpot.objects.all()
		for place in all_places:
			if (place.lat_lmt_min <= user_pos.latitude <= place.lat_lmt_max) and (place.lng_lmt_min <= user_pos.longitude <= place.lng_lmt_max):
				return (place_indicator,place)
			else:
				pass
		place_indicator = False
		return (place_indicator,0)

	if request.method == 'POST':
		pstn_1 = Position(user=request.user, latitude=request.POST.get('lat'), longitude=request.POST.get('lng'));
		pstn_1.save() #Add the newly created position object into the liveudpate list
		all_updates = LiveUpdate.objects.all().order_by('date_time')
		if (len(all_updates) == 10):
			all_updates[0].delete()
			new_liveupdate = LiveUpdate(username=pstn_1.user.username)
			if find_pos(pstn_1.user)[0]:
				new_liveupdate.place = find_pos(pstn_1.user)[1]
			new_liveupdate.save()
		else:
			new_liveupdate = LiveUpdate(username=pstn_1.user.username)
			if find_pos(pstn_1.user)[0]:
				new_liveupdate.place = find_pos(pstn_1.user)[1]
			new_liveupdate.save()

	ancestor_place = MugSpot.objects.filter(id=place_id)
	user_1 = request.user 
	user_indicator = 0 # Used to check if the user is logged in 
	if (user_1.is_authenticated()):
		user_indicator = 1
	else:
		user_indicator = 0
	sessions = Session.objects.all().order_by('-expire_date')
	live_update_list = LiveUpdate.objects.all().order_by('date_time')
	"""
	all_curr_users_p = []
	all_curr_users = []
	for session in sessions:
		data = session.get_decoded()
		user_s = User.objects.filter(id=data['_auth_user_id'])[0]
		res_find_pos = find_pos(user_s) #Determine the user's location to be within the mugspots or outside the mugspots
		if res_find_pos == "No position object yet":
			pass
		else:
			user_p = Position.objects.filter(user=user_s)[0]
			all_curr_users_p.append(user_p)
			all_curr_users.append(user_s.username)
			"""
	if (len(ancestor_place)>0):
		list_places = MugSpot.objects.filter(ancestor_spot=ancestor_place[0]).order_by('-spot_name')
		return render(request, 'mugspot/index.html', {
				'list_places':list_places,
				'place':ancestor_place[0].__str__,
				'user_indicator': user_indicator,
				'username': user_1.username,
				'live_update_list': live_update_list,
			})
	else: 
		list_places = MugSpot.objects.filter(ancestor_spot=None).order_by('-spot_name')
		return render(request, 'mugspot/index.html', {
				'list_places':list_places,
				'place':'NUS',
				'user_indicator': user_indicator,
				'username': user_1.username,
				'live_update_list': live_update_list,
			})
def about(request, place_id=0):
 	return render_to_response('mugspot/about.html')

def register(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		user_form = UserRegisterForm(request.POST)
		# check whether it's valid:
		if user_form.is_valid():
			if user_form.clean():
				user = User.objects.create_user(username=user_form.cleaned_data['username'],
					email=user_form.cleaned_data['user_email'],
					password=user_form.cleaned_data['user_password'],
					is_staff=False,
					is_active=True,
					)
				person = Person(user=user,
					faculty=user_form.cleaned_data['user_faculty'],
					)
				person.save()
				return HttpResponseRedirect(reverse('mugspot:index'))
			else:
				user_form.clean()
	# if a GET (or any other method) we'll create a blank form
	else:
		user_form = UserRegisterForm()

	return render(request, 'mugspot/register.html', {'user_form': user_form})

def login_view(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		login_form = UserLoginForm(request.POST)
		# check whether it's valid
		if login_form.is_valid():
			user = authenticate(username=login_form.cleaned_data['user_name'], 
				password=login_form.cleaned_data['user_password'],)
			if user is not None:
				if user.is_active: # User is correct and active
					login(request,user)
					return HttpResponseRedirect(reverse('mugspot:index'))
				else: # User is correct but not active
					login_form = UserLoginForm()
					return render(request, 'mugspot/login.html', {'user_form': login_form})
			else: # Username/password is incorrect
				login_form = UserLoginForm()
				return render(request, 'mugspot/login.html', {'user_form': login_form})
	else: #Create a blank login form
		login_form = UserLoginForm()
		return render(request, 'mugspot/login.html', {'user_form': login_form})		

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('mugspot:login'))

def all_positions_view(request):
	all_pos = Position.objects.all()
	data = serializers.serialize("json", all_pos)
	return HttpResponse(data, content_type='application/json')

def check_login_js_view(request):
	user_1 = request.user
	indicator = 0
	if (user_1.is_authenticated()):
		all_pos = Position.objects.all()
		for position in all_pos:
			if position.user.username == user_1.username:
				indicator = 2
				break
			indicator = 1
	else: 
		pass
	response = JsonResponse({'indicator': indicator})
	return response

	
