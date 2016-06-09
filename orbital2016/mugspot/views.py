from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
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

def register(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		user_form = UserRegisterForm(request.POST)
		# check whether it's valid:
		if user_form.is_valid():
			if user_form.clean():
				user = Person()
				user.username = user_form.cleaned_data['username']
				user.user_email = user_form.cleaned_data['user_email']
				user.user_faculty = user_form.cleaned_data['user_faculty']
				user.user_password = user_form.cleaned_data['user_password']
				user.save()
				return HttpResponseRedirect(reverse('mugspot:index'))
			else:
				user_form.clean()
	# if a GET (or any other method) we'll create a blank form
	else:
		user_form = UserRegisterForm()

	return render(request, 'mugspot/register.html', {'user_form': user_form})

def login(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		login_form = UserLoginForm(request.POST)
		# check whether it's valid
		if login_form.is_valid():
			get_email = Person.objects.filter(user_email=login_form.cleaned_data['user_email'])
			if len(get_email) == 0:
				pass
			else:
				# declare the user to be logging in
				# take the user to the homepage