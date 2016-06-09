from __future__ import unicode_literals

from django.db import models

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
	def __str__(self):
		return self.spot_name

class Person(models.Model):
	friends = models.ManyToManyField('self', blank=True)
	username = models.CharField(max_length=200)
	user_email = models.EmailField(max_length=254)	
	user_faculty = models.CharField(max_length=200)
	user_password = models.CharField(max_length=200)
	def __str__(self):
		return self.username
