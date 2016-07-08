from django.contrib import admin

# Register your models here.
from .models import MugSpot, Person, Position

class MugSpotAdmin(admin.ModelAdmin):
	def save_model(self,request,obj,form,change):
		if change == False:
			if obj.ancestor_spot == None: 
				obj.detail_lvl = 1
			else:
				obj.detail_lvl = obj.ancestor_spot.detail_lvl + 1
		else:
			pass
		obj.save()
		max_dtl_lvl = max(spot.detail_lvl for spot in MugSpot.objects.all())
		for i in range(max_dtl_lvl):
			ls = MugSpot.objects.filter(detail_lvl=max_dtl_lvl-i).order_by('-id')
			for ls_element in ls:
				all_children = MugSpot.objects.filter(ancestor_spot=ls_element)
				if len(all_children) == 0:
					pass
				else:
					all_capacity = [o.capacity for o in all_children]
					all_occupied = [o.occupied for o in all_children]
					ls_element.capacity = sum(all_capacity)
					ls_element.occupied = sum(all_occupied)
					ls_element.save()

admin.site.register(MugSpot, MugSpotAdmin)
admin.site.register(Person)
admin.site.register(Position)