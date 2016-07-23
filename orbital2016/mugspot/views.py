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
from .models import MugSpot, Person, Position, LiveUpdate, FriendUpdate, FriendRequest
from .forms import UserRegisterForm, UserLoginForm, AccountDetailForm, LocationForm

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
				'user': user_1,
			})
	else: 
		list_places = MugSpot.objects.filter(ancestor_spot=None).order_by('-spot_name')
		return render(request, 'mugspot/index.html', {
				'list_places':list_places,
				'place':'NUS',
				'user_indicator': user_indicator,
				'username': user_1.username,
				'live_update_list': live_update_list,
				'user': user_1,
			})
@login_required # Still incomplete -- research more
def user_profile_view(request, user_id=0):
	""" Handle request for user's account page """
	user = User.objects.filter(id=user_id)[0]
	stalker = request.user 
	user_indicator = 0 # Used to check if the user is logged in 
	if (stalker.is_authenticated()):
		user_indicator = 1
	else:
		user_indicator = 0
	# show a form with data from database for 'GET' request
	if request.method == 'GET':
		person = Person.objects.filter(user=user)[0]
		account_form = AccountDetailForm(initial={
			'user_name': user.username,
			'user_email': user.email,
			'user_faculty': person.faculty,
		}) # Display user account detail

		location_form = LocationForm() # Display location box for user to type into

		live_update_list = LiveUpdate.objects.all().order_by('date_time') # Display live update list

		friend_update_list = FriendUpdate.objects.filter(receiver=user).order_by('date_time') # Display friend update list
		if len(friend_update_list) > 20:
			friend_update_list = friend_update_list[:20]

		friend_request_list = FriendRequest.objects.filter(receiver=user).order_by('-date_time') # Display friend request list

		friend_list = person.friends.all() # Display all friends list

		addfriend_indicator = 0 # Help decide the status of the add friend button
		person_2 = Person.objects.filter(user=stalker)[0]
		if (person_2 in friend_list):
			addfriend_indicator = 2 # stalker and user whose profile being shown are friends
		else:
			relevant_request = FriendRequest.objects.filter(sender=stalker,receiver=user)
			if len(relevant_request) == 0:
				addfriend_indicator = 0 # stalker has not added user whose profile is being shown as a friend
			else:
				addfriend_indicator = 1 # stalker has added user whose profile is being shown as a friend

		return render(request, 'mugspot/userprofile.html', {
				'live_update_list':live_update_list,
				'friend_update_list': friend_update_list,
				'location_form': location_form,
				'account_form': account_form,
				'friend_list': friend_list,
				'friend_request_list': friend_request_list,
				'user_prof': user,
				'stalker': stalker,
				'user_indicator': user_indicator,
				'addfriend_indicator': addfriend_indicator,
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
		if len(all_pos) == 0:
			indicator = 1
		for position in all_pos:
			if position.user.username == user_1.username:
				indicator = 2
				break
			indicator = 1
	else: 
		pass
	response = JsonResponse({'indicator': indicator})
	return response

def update_friends_view(request):
	if request.method == 'POST':
		user = request.user
		person_user = Person.objects.filter(user=user)[0]
		friendlist = person_user.friends.all()
		if request.POST.get("yes") == 1:
			for friend in friendlist:
				request = FriendUpdate(sender=user,receiver=friend.user,mug_spot=request.POST.get('location_name'))
				request.save()
		else:
			for friend in friendlist:
				request = FriendUpdate(sender=user,receiver=friend.user,mug_spot=request.POST.get('location_name'),status=False)
				request.save()
		return HttpResponseRedirect(reverse('mugspot:user_profile_view', kwargs={'user_id': user.id}))

def accept_request_view(request):
	user = request.user
	if request.method == 'POST':
		sender = request.POST.get('user_name')
		sender = User.objects.filter(username=sender)[0]
		request = FriendRequest.objects.filter(sender=sender,receiver=user)[0]
		request.delete()
		person_sender = Person.objects.filter(user=sender)[0]
		person_receiver = Person.objects.filter(user=user)[0]
		person_sender.friends.add(person_receiver)
		person_receiver.friends.add(person_sender)
		return HttpResponse("Add Friend Succeeded!")
	else:
		return HttpResponse("Go away guys, nothing to see here!")

def delete_request_view(request):
	user = request.user
	if request.method == 'POST':
		sender = request.POST.get('user_name')
		sender = User.objects.filter(username=sender)[0]
		request = FriendRequest.objects.filter(sender=sender,receiver=user)[0]
		request.delete()
		return HttpResponse("Delete Request Succeeded!")
	else:
		return HttpResponse("Go away guys, nothing to see here!")


def create_request_view(request):
	if request.method == 'POST':
		sender = request.POST.get('sender')
		sender = User.objects.filter(username=sender)[0]
		receiver = request.POST.get('receiver')
		receiver = User.objects.filter(username=receiver)[0]
		request = FriendRequest(sender=sender, receiver=receiver, sender_consent=True)
		request.save()
		return HttpResponse("Created Request Succeeded! Sender: " + sender.username + ", Receiver: " + receiver.username)
	else:
		return HttpResponse("Go away guys, nothing to see here!")

def undo_request_view(request):
	sender = request.user.username
	if request.method == 'POST':
		receiver = request.POST.get('receiver_name')
		sender = User.objects.filter(username=sender)[0]
		receiver = User.objects.filter(username=receiver)[0]
		request = FriendRequest.objects.filter(sender=sender,receiver=receiver)
		request.delete()
		response = JsonResponse({'sender': sender.username, 'receiver': receiver.username})
		return response
	else:
		return HttpResponse("Go away guys, nothing to see here!")

def update_account_view(request):
	user = request.user
	if request.method == 'POST':
			# create a form instance and populate it with data from the request
			person = Person.objects.filter(user=user)[0]
			user.username = request.POST.get('user_name')
			user.email = request.POST.get('user_email')
			person.faculty = request.POST.get('user_faculty')
			user.save()
			person.save()
			return HttpResponseRedirect(reverse('mugspot:user_profile_view', kwargs={'user_id': user.id}))
		# if a GET (or any other method) we'll create a blank form
	else:
		return HttpResponse("Go away guys! Nothing to see here! :P")

def edit_profile_view(request, user_id=0):
	""" Handle request for user's account edit page """
	user = User.objects.filter(id=user_id)[0]
	stalker = request.user
	if stalker != user:
		return HttpResponse("Go away guys, nothing to see here!")
	else:
		user_indicator = 0 # Used to check if the user is logged in 
		if (stalker.is_authenticated()):
			user_indicator = 1
		else:
			user_indicator = 0
		# show a form with data from database for 'GET' request
		if request.method == 'GET':
			person = Person.objects.filter(user=user)[0]
			account_form = AccountDetailForm(initial={
				'user_name': user.username,
				'user_email': user.email,
				'user_faculty': person.faculty,
			}) # Display user account detail
			account_form.fields['user_name'].disabled = False
			account_form.fields['user_email'].disabled = False
			account_form.fields['user_faculty'].disabled = False

			location_form = LocationForm() # Display location box for user to type into

			live_update_list = LiveUpdate.objects.all().order_by('date_time') # Display live update list

			friend_update_list = FriendUpdate.objects.filter(receiver=user).order_by('date_time') # Display friend update list

			friend_request_list = FriendRequest.objects.filter(receiver=user).order_by('-date_time') # Display friend request list

			friend_list = person.friends.all() # Display all friends list

			addfriend_indicator = 0 # Help decide the status of the add friend button
			person_2 = Person.objects.filter(user=stalker)[0]
			if (person_2 in friend_list):
				addfriend_indicator = 2 # stalker and user whose profile being shown are friends
			else:
				relevant_request = FriendRequest.objects.filter(sender=stalker,receiver=user)
				if len(relevant_request) == 0:
					addfriend_indicator = 0 # stalker has not added user whose profile is being shown as a friend
				else:
					addfriend_indicator = 1 # stalker has added user whose profile is being shown as a friend

			return render(request, 'mugspot/userprofile_edit.html', {
					'live_update_list':live_update_list,
					'friend_update_list': friend_update_list,
					'location_form': location_form,
					'account_form': account_form,
					'friend_list': friend_list,
					'friend_request_list': friend_request_list,
					'user_prof': user,
					'stalker': stalker,
					'user_indicator': user_indicator,
					'addfriend_indicator': addfriend_indicator,
				})
	
