from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django import forms
from django.forms import ModelForm
from boysdinner.models import Person, Dish, DishVote
import datetime
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelChoiceField
from django.utils.timezone import get_current_timezone


# Create your views here.

class IndexView(TemplateView):
	template_name = "boysdinner/index.html"

class PersonForm(ModelForm):
	class Meta:
		model = Person
		widgets = {
			'first_name': forms.TextInput({'placeholder': 'First name'})
		}
		fields = ['first_name']

class MyModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s" % obj.first_name.title()

class SearchForm(ModelForm):
	try:
		person_dropdown = MyModelChoiceField(queryset= Person.objects.filter(
														dish__served_date=datetime.date.today()
																			), 
										empty_label="--Find yourself--", 
										widget=forms.Select(attrs={"onChange":'submit()'}))
	except:
		person_dropdown = "None"

	class Meta:
		model = Person
		fields = ['person_dropdown']

class ResultsModelChoiceField(ModelChoiceField):
	#this subclass exists only to change the way the option string is displayed
	def label_from_instance(self, obj):
		try:
			served_date = obj.served_date.strftime("%A %B %d, %Y")
		except:
			served_date=""

		return "%s" %served_date

class DatedResultsForm(ModelForm):
	#dropdown with all dates where there were votes
	dated_results_dropdown = ResultsModelChoiceField(

					#returns queryset
					queryset = Dish.objects.all().order_by('served_date').distinct(), 
					#returns dict
					#queryset = Dish.objects.all().order_by('served_date').values_list('served_date', flat=True).distinct(), 
					#queryset = Dish.objects.all().order_by('served_date').values_list('id','served_date').distinct(), 
					empty_label="--View past results--", 
					widget=forms.Select(attrs={"onChange":'submit()'}))
									
	class Meta:
		model = Dish
		fields = ['dated_results_dropdown']

class DishForm(ModelForm):
	dish_name = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 
										'rows': 3,'placeholder': 'Dish name'}))
	class Meta:
		model = Dish
		fields = ['id','dish_name','current_dish']

class DishVoteForm(ModelForm):
	comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 5}))
	fake_id = forms.CharField(widget=forms.HiddenInput())
	class Meta:
		model = DishVote
		widgets = {
			'comment': forms.TextInput({'placeholder': 'Penny for your thoughts'})
		}
		fields = ['taste_rating','originality_rating',
					'presentation_rating','comment']
		labels = {
				'taste_rating': _('Taste Rating (1-10):'),
				'originality_rating': _('Originality Rating (1-5):'),
				'presentation_rating': _('Presentation Rating (1-5):'),
				}

def signin(request, first_name='', dish_name=''):
	first_name = first_name.lower()
	dish_name = dish_name.lower()
	error_message=""
	dish_name = dish_name.replace('_',' ')
	is_current=""
	persons = {}
	voter_id=''
	if request.method == "POST":
		form1 = PersonForm(request.POST)
		form2 = DishForm(request.POST)
		#check if form is valid
		if form1.is_valid() and form2.is_valid():
			person_name = form1.cleaned_data['first_name'].lower()
			dish_name = form2.cleaned_data['dish_name'].lower()
			current_dish = form2.cleaned_data['current_dish']
			found_person=""
			try:
				found_person = Person.objects.get(first_name=person_name)

			#this person is not in database create a new person
			except:
				new_person = form1.save(commit=False)
				new_person.first_name = person_name
				new_person.save()
				new_persons_dish = form2.save(commit=False)
				new_persons_dish = dish_name
				new_persons_dish.chef=new_person
				new_persons_dish.served_date=datetime.date.today()

				#If this is current dish, remove current status for all other dishes
				if current_dish:
					Dish.objects.all().update(current_dish=False)
					new_persons_dish.current_dish = current_dish

				new_persons_dish.save()
				voter_id = new_person.id

			#name does exist so update its dish if served today
			else:
				voter_id = found_person.id
				try:
					#get associated dish object
					todays_dish = Dish.objects.get(chef=found_person, served_date=datetime.date.today())
				#if dish exists but served on day other than today then create new dish for today
				except:
					#this is a new dish (dated for today) for existing person
					new_dish = form2.save(commit=False)
					#new_dish.dish_name = dish_name
					#now associate found_person with new dish
					new_dish.chef=found_person
					new_dish.served_date=datetime.date.today()
					#If this is current dish, remove current status for all other dishes
					if current_dish:
						Dish.objects.all().update(current_dish=False)
						new_dish.current_dish = current_dish
					new_dish.save()
					voter_id = found_person.id
				#if there exists a dish for this person served today then allow for update
				else:
					#update wording of today's dish name
					todays_dish.dish_name=dish_name
					#If this is current dish, remove current status for all other dishes
					if current_dish:
						Dish.objects.all().update(current_dish=False)
						todays_dish.current_dish = current_dish
					todays_dish.save()
					#if dish exists but served on day other than today then create new dish for today
						
			finally:
				return HttpResponseRedirect(reverse('boysdinner:vote',args=(voter_id,)))
		#form not valid:
		else:
			error_message = "Please fill all fields"
			search_form = SearchForm()

	#arrival NOT by post
	else:
		if first_name=="a":
			first_name=""
			dish_name=""
		pre_pop = {'first_name':first_name.title(),'dish_name':dish_name.title()}
		form1 = PersonForm(initial=pre_pop)
		form2 = DishForm(initial=pre_pop)
		search_form = SearchForm()
	try:
		persons = Person.objects.all()
	except:
		persons = {'first_name':'No one has logged in'}
	return render(request, 'boysdinner/index.html', 
					{'form1': form1, 
					'form2': form2,
					'search_form': search_form,
					'is_current': is_current,
					'error_message': error_message,
					'persons': persons
					}
				)

def search_person(request):
	#if post then search
	#if not post (or 1st time on page) then show page again
	pre_pop = {}
	found_person=''
	search_error=''
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			try:
				#Find record (from dropdown) in database if it exists
				first_name = form.cleaned_data['person_dropdown'].first_name.lower()
				found_person = Person.objects.get(first_name=first_name)
				pre_pop['name']=found_person.first_name
				found_dish = Dish.objects.get(chef_id=found_person, served_date=datetime.date.today)
				pre_pop['dish'] = found_dish.dish_name.replace(' ','_')

				return HttpResponseRedirect(reverse('boysdinner:signin',args=(pre_pop['name'],pre_pop['dish'])))
			except:
				search_error="Misspelled name or no such user"
		else:
			search_error="Enter a name damnit!!"

	form1 = PersonForm()
	form2 = DishForm()
	search_form = SearchForm()
	is_current= False
	error_message=""

	return render(request, 'boysdinner/index.html', 
					{'form1': form1, 
					'form2': form2,
					'search_form': search_form,
					'is_current': is_current,
					'pre_pop': pre_pop,
					'search_error': search_error,
					'error_message': error_message
					}
				)

def old_votes(request, voter_id, pre_fix):
	error_message=""
	message=""
	chef_name=""
	old_votes_message=""
	is_current = False
	vote_list= []
	form0=''
	#look through database for all dishvotes with this guy's id
	#enumerate them vote1, vote2, etc. while vote is the newest one
	if request.method == "POST":
		#Process remaining forms
		votes = [DishVoteForm(request.POST, prefix=str(x)) for x in range(int(pre_fix))]
		flag="good"
		if all([vt.is_valid() for vt in votes]):
			for vt in votes:
				old_vote = vt.save(commit=False)
				if old_vote.taste_rating>10:
					flag="bad"
					error_message = "taste rating must be from 1 to 10"
				elif old_vote.originality_rating>5:
					flag="bad"
					error_message = "originality rating must be from 1 to 5"
				elif old_vote.presentation_rating>5:
					flag="bad"
					error_message = "presentation rating must be from 1 to 5"
				#everything is good go ahead and commit to database
				if flag=="good":
					#get primary key
					pk = int(vt.cleaned_data['fake_id'])
					editable_vote = DishVote.objects.get(pk=pk)
					editable_vote.taste_rating = old_vote.taste_rating
					editable_vote.originality_rating = old_vote.originality_rating
					editable_vote.presentation_rating = old_vote.presentation_rating
					editable_vote.comment = old_vote.comment
					editable_vote.save()
			return HttpResponseRedirect(reverse('boysdinner:vote', args=(voter_id,)))

				
		#submit but old votes invalid (not fully/correctly filled)
		else:
			try:
				voted_upon = Dish.objects.filter(current_dish=True)[0]
				chef_name = voted_upon.chef.first_name
			except:
				error_message = "Try again maybe from the beginning"
			error_message = "Please vote all fields"

	#arrived but not via post------------------------------
	else:
		#arriving at the page for 1st time
		#Find name of current chef being voted on and determine if current user is that person
		try:
			#[0] ensures that only the most recent record gets brought up
			chef = Dish.objects.filter(current_dish=True)[0].chef
			chef_name = chef.first_name
			if int(voter_id)==int(chef.id):
				#displayed when current voting disabled
				message = "Your head is currently on the voting bloc"
				is_current = True
		except:
			#No one has indicated that they are being voted upon
			message = "No Chef is currently on the voting bloc"

		#create newest and blank form that is to appear on top of page
		form0 = DishVoteForm(prefix=str(0))
		# Find old votes
		try:
			#find other votes made
			dish_votes = DishVote.objects.filter(critic_id=voter_id)
			count = 1
			for old_vote in dish_votes:
				taste_rating = old_vote.taste_rating
				originality_rating = old_vote.originality_rating
				presentation_rating = old_vote.presentation_rating
				comment = old_vote.comment
				pre_pop = {'taste_rating':taste_rating,
						'originality_rating':originality_rating,
						'presentation_rating':presentation_rating,
						'comment':comment}
				form = DishVoteForm(initial=pre_pop, prefix=str(count))
				vote_list.append(form)
				count+=1
		except:
			old_votes_message = "You have no old votes"
		#produce dictionary of forms based on query of dbase

	return render(request, 'boysdinner/myvotes.html',
					{'form0':form0,
					'vote_list':vote_list,
					'voter_id':voter_id,
					'chef_name':chef_name,
					'is_current':is_current,
					'message':message,
					'old_votes_message':old_votes_message,
					'error_message':error_message
					}
				)

def vote(request, voter_id):
	error_message=""
	message=""
	chef_name=""
	dish_info=[]
	old_votes_message=""
	is_current = False
	vote_list= []
	form0=''
	pre_fix=0
	voter_name = ""
	#look through database for all dishvotes with this guy's id
	#enumerate them vote1, vote2, etc. while vote is the newest one
	if request.method == "POST":
		flag="good"
		newest_vote = DishVoteForm(request.POST)
		if newest_vote.is_valid():
			newest_vote = newest_vote.save(commit=False)
			new_id = newest_vote.id
			if newest_vote.taste_rating>10:
				flag="bad"
				error_message = "taste rating must be from 1 to 10"
			elif newest_vote.originality_rating>5:
				flag="bad"
				error_message = "originality rating must be from 1 to 5"
			elif newest_vote.presentation_rating>5:
				flag="bad"
				error_message = "presentation rating must be from 1 to 5"
			#everything is good go ahead and commit to database
			if flag=="good":
				#associate current voter as the critic
				newest_vote.critic = Person.objects.get(id=voter_id)
				try:
					#associate this vote to whichever dish (if any) is currently on voting block
					newest_vote.dish = Dish.objects.filter(current_dish=True)[0]
				except Exception as e:
					error_message = "No dish currently on voting bloc"
				#now try to save (assuming there was a dish on the block)
				try:
					newest_vote.save()
				#if vote didn't save for whatever reason
				except:
					error_message = "Unable to save this vote"
				#if saved then go to results page
				else:
					return HttpResponseRedirect(reverse('boysdinner:results', args=(voter_id,)))

				
		#submit but form invalid (not fully filled)
		else:
			try:
				voted_upon = Dish.objects.filter(current_dish=True)[0]
				chef_name = voted_upon.chef.first_name
			except:
				error_message = "Try again maybe from the beginning"
			error_message = "Please vote all fields"

	#arrived but not via post------------------------------
	#Find name of current chef being voted on and determine if current user is that person
	try:
		#[0] ensures that only the most recent record gets brought up
		chef = Dish.objects.filter(current_dish=True, served_date=datetime.date.today())[0].chef
		chef_name = chef.first_name
		if int(voter_id)==int(chef.id):
			#displayed when current voting disabled
			message = "Your head is currently on the voting bloc"
			is_current = True
	except:
		#No one has indicated that they are being voted upon
		message = "No Chef is currently on the voting bloc"

	#create newest and blank form that is to appear on top of page
	form0 = DishVoteForm(initial={'fake_id':'0'})
	# Find old votes
	count=0
	try:
		#find other votes made by this person
		voter_name = Person.objects.filter(pk=voter_id)[0].first_name
		dish_votes = DishVote.objects.filter(critic_id=voter_id, dish__served_date=datetime.date.today())
	except:
		old_votes_message = "You have no old votes"
	#there are old votes
	else:
		if not dish_votes:
			old_votes_message = "You have no old votes"
		count = 0
		for old_vote in dish_votes:
			taste_rating = old_vote.taste_rating
			originality_rating = old_vote.originality_rating
			presentation_rating = old_vote.presentation_rating
			fake_id = old_vote.id
			comment = old_vote.comment
			done_chef_name= old_vote.dish.chef.first_name
			dish_name= old_vote.dish.dish_name
			pre_pop = {'taste_rating':taste_rating,
					'originality_rating':originality_rating,
					'presentation_rating':presentation_rating,
					'fake_id':fake_id,
					'comment':comment}
			form = DishVoteForm(initial=pre_pop, prefix=str(count))
			details = {'done_chef_name':done_chef_name, 'dish_name':dish_name}
			bundle = {'form':form, 'details':details}
			vote_list.append(bundle)
			count+=1
	#Tells old_votes method how many prefixes there are
	voter_id = int(voter_id)
	pre_fix = count

	return render(request, 'boysdinner/myvotes.html',
					{'form0':form0,
					'vote_list':vote_list,
					'voter_id':voter_id,
					'voter_name':voter_name,
					'chef_name':chef_name,
					'dish_info':dish_info,
					'is_current':is_current,
					'message':message,
					'old_votes_message':old_votes_message,
					'pre_fix':pre_fix,
					'error_message':error_message
					}
				)

def results(request, voter_id):
	#get results only for today
	served_date = datetime.date.today()
	voter_name=""
	vote_dish = ""
	raw_served_date = ""

	#process form for drop down acknowledging date selection
	if request.method == "POST":
		#form for queries for dish dates
		#then get dish_dates and use their dish_ids to pull all related info
		form = DatedResultsForm(request.POST)
		if form.is_valid():
			#get date selection
			try:
				served_date = form.cleaned_data['dated_results_dropdown'].served_date
			except:
				served_date = datetime.date.today()

	#dictionary Shows voting results for each person on given date
	try:
		dish_list = Dish.objects.filter(served_date=served_date)
		vote_list = DishVote.objects.filter(dish=dish_list)
		#just for displaying name
		voter_name = Person.objects.filter(id=voter_id)[0].first_name
	except:
		error_message="There are currently no votes"

	taste_rating = 0
	originality_rating = 0
	presentation_rating = 0
	vote_count = 0
	totals_list=[]
	for dish in dish_list:
		for vote in vote_list:
			if vote.dish == dish:
				taste_rating+= vote.taste_rating
				originality_rating+= vote.originality_rating
				presentation_rating+= vote.presentation_rating
				vote_count+=1
				vote_dish = vote.dish

		#capture the info for the dish's vote
		if vote_dish == dish:
			total={}
			total['chef_name']=dish.chef.first_name
			total['chef_id']=int(dish.chef.id)
			total['overall_score']=taste_rating+originality_rating+presentation_rating
			total['vote_count']=vote_count
			totals_list.append(total)
			taste_rating= 0
			originality_rating=0
			presentation_rating=0
			vote_count=0

	#create the populated dropdown for results page
	dated_form = DatedResultsForm()

	raw_served_date = str(served_date).replace('-','x')

	if served_date==datetime.date.today():
 		served_date = "today"
	else:
		try:
			served_date = served_date.strftime("%B %d, %Y")
		except:
			served_date = ""
	if voter_name:
		voter_name = "%s, " %voter_name.title()
	else:
		voter_name = ""

	if totals_list:
		greeting = "%sthe vote totals for <b>%s</b> are below" %(voter_name, served_date)
	else:
		greeting = "There was no voting <b>%s</b>" %(served_date)

	user_id = int(voter_id)

	#populates old dinner competition dropdown
	try:
		old_dinners_list = Dish.objects.all().order_by('served_date')
	except:
		old_dinners_list = "There are no old dates"

	#



	return render(request, 'boysdinner/results.html',
					{'totals_list': totals_list,
					'voter_id': voter_id,
					'user_id': user_id,
					'dated_form': dated_form,
					'served_date': served_date,
					'raw_served_date': raw_served_date,
					'old_dinners_list': old_dinners_list,
					'greeting': greeting
					}
				)


def my_critics(request, user_id, raw_served_date):
	raw_served_date = raw_served_date.replace('x','-')
	#fetch all criticisms associated with current user for only today's voting
	dish_votes=""
	if not raw_served_date:
		raw_served_date = datetime.date.today()

	try:
		dish_votes = DishVote.objects.filter(
								dish__chef__id=user_id, 
								#dish__served_date=datetime.date.today()
								dish__served_date=raw_served_date
										)
	except:
		print("NO CURRENT CRITICISMS")

	return render(request, 'boysdinner/mycritics.html',
					{'dish_votes': dish_votes,
					'user_id': user_id,
					'voter_id': user_id
					}
				)
