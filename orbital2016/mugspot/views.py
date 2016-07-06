from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .models import MugSpot, Person
from .forms import UserRegisterForm, UserLoginForm

def index(request, place_id=0):
	# Need to add the feature check if the user is logged in here
	ancestor_place = MugSpot.objects.filter(id=place_id)
	if (len(ancestor_place)>0):
		list_places = MugSpot.objects.filter(ancestor_spot=ancestor_place[0]).order_by('-spot_name')
		return render(request, 'mugspot/index.html', {
				'list_places':list_places,
				'place':ancestor_place[0].__str__,
			})
	else: 
		list_places = MugSpot.objects.filter(ancestor_spot=None).order_by('-spot_name')
		return render(request, 'mugspot/index.html', {
				'list_places':list_places,
				'place':'NUS',
			})

@login_required(login_url='mugspot:login')
def logged_in_index(request, place_id=0):
	# Need to add the feature check if the user is logged in here
	ancestor_place = MugSpot.objects.filter(id=place_id)
	if (len(ancestor_place)>0):
		list_places = MugSpot.objects.filter(ancestor_spot=ancestor_place[0]).order_by('-spot_name')
		return render(request, 'mugspot/loggedinindex.html', {
				'list_places':list_places,
				'place':ancestor_place[0].__str__,
			})
	else: 
		list_places = MugSpot.objects.filter(ancestor_spot=None).order_by('-spot_name')
		return render(request, 'mugspot/loggedinindex.html', {
				'list_places':list_places,
				'place':'NUS',
			})

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
				if user.is_active:
					login(request,user)
					return HttpResponseRedirect(reverse('mugspot:loggedinindex'))
				else:
					login_form = UserLoginForm()
					return render(request, 'mugspot/login.html', {'user_form': login_form})
			else:
				login_form = UserLoginForm()
				return render(request, 'mugspot/login.html', {'user_form': login_form})
	else: #Create a blank login form
		login_form = UserLoginForm()
		return render(request, 'mugspot/login.html', {'user_form': login_form})		

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('mugspot:index'))
