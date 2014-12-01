from django.db import models

# Create your models here.

class Person(models.Model):
	#Changed Chefs and Critics into just Person table
	first_name = models.CharField(max_length=50)

	def __str__(self):
		return self.first_name

class Dish(models.Model):
	chef = models.ForeignKey(Person)
	dish_name = models.CharField(max_length=200)
	current_dish = models.BooleanField(default=False)
	served_date = models.DateField('Date Dish Served')
	#served_date = models.DateField('Date Dish Served',auto_now=True)

	def __str__(self):
		return self.chef.first_name+"'s "+self.dish_name

class DishVote(models.Model):
	dish = models.ForeignKey(Dish)
	critic = models.ForeignKey(Person, null=True)
	taste_rating = models.IntegerField(default=0)
	originality_rating = models.IntegerField(default=0)
	presentation_rating = models.IntegerField(default=0)
	comment = models.CharField(max_length=400,null=True, blank=True)

	def __str__(self):
		return self.critic.first_name+"'s voting record"

	class Meta:
		unique_together = (('critic', 'dish'),)
