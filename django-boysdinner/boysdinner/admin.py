from django.contrib import admin
from boysdinner.models import Person, Dish, DishVote

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
	fields =['first_name']
	list_display=('id','first_name',)

admin.site.register(Person, PersonAdmin)

class DishAdmin(admin.ModelAdmin):
	fields =['chef', 'dish_name', 'current_dish','served_date']
	list_display=('chef', 'dish_name', 'current_dish','served_date')

admin.site.register(Dish, DishAdmin)

class DishVoteAdmin(admin.ModelAdmin):
	fields =['critic','dish','taste_rating', 'originality_rating', 'presentation_rating','comment']
	list_display=('critic','dish','taste_rating', 'originality_rating', 'presentation_rating','comment')

admin.site.register(DishVote, DishVoteAdmin)
