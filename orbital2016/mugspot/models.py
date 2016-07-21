from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

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
	date_time = models.DateTimeField(default=timezone.now)
	duration = models.DurationField(default=timedelta(hours=1))

class LiveUpdate(models.Model):
	username = models.CharField(max_length=200, default="")
	status = models.BooleanField(default=True)
	date_time = models.DateTimeField(default=timezone.now)
	place = models.OneToOneField(MugSpot,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
		)

class FriendUpdate(models.Model):
	sender = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		default=None,
		related_name='+',
		)
	receiver = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		default=None,
		related_name='+',
		)
	status = models.BooleanField(default=True)
	date_time = models.DateTimeField(default=timezone.now)
	mug_spot = models.CharField(default="", max_length=200)

class FriendRequest(models.Model):
	sender = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		default=None,
		related_name='+',
		)
	receiver = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		default=None,
		related_name='+',
		)
	sender_consent = models.BooleanField(default=False)
	receiver_consent = models.BooleanField(default=False)
	date_time = models.DateTimeField(default=timezone.now)
