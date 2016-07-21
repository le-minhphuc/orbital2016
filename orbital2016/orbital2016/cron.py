from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from mugspot.models import MugSpot, Person, Position, LiveUpdate
from django.utils import timezone
from datetime import timedelta

def scheduled_position_check():
	all_pos = Position.objects.all()
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

	for pstn_1 in all_pos: 
		if (timezone.now() >= pstn_1.date_time + pstn_1.duration):
			all_updates = LiveUpdate.objects.all().order_by('date_time')
			if (len(all_updates) == 10):
				all_updates[0].delete()
				new_liveupdate = LiveUpdate(username=pstn_1.user.username, status=False)
				if find_pos(pstn_1.user)[0]:
					new_liveupdate.place = find_pos(pstn_1.user)[1]
				new_liveupdate.save()
			else:
				new_liveupdate = LiveUpdate(username=pstn_1.user.username, status=False)
				if find_pos(pstn_1.user)[0]:
					new_liveupdate.place = find_pos(pstn_1.user)[1]
				new_liveupdate.save()
			pstn_1.delete()
		else:
			pass
