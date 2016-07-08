from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MugSpot(models.Model):
	ancestor_spot = models.ForeignKey(
		'self',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		)
	spot_name = models.CharField(max_length=200)
	capacity = models.IntegerField(default=0)
	occupied = models.IntegerField(default=0)
	detail_lvl = models.IntegerField(default=0)
	lat_lmt_min = models.FloatField(default=0)
	lat_lmt_max = models.FloatField(default=0)
	lng_lmt_min = models.FloatField(default=0)
	lng_lmt_max = models.FloatField(default=0)
	def __str__(self):
		return self.spot_name

class Person(models.Model):
	user = models.OneToOneField(User,
							on_delete=models.CASCADE,
							primary_key=True,
							default=None,
							)
	friends = models.ManyToManyField('self', blank=True, default=None)
	faculty = models.CharField(max_length=200, default=None)
	def __str__(self):
		return self.user.username

class Position(models.Model):
	user = models.OneToOneField(User,
		on_delete=models.CASCADE,
		primary_key=True,
		default=None,
		)
	latitude = models.FloatField(default=0)
	longitude = models.FloatField(default=0)