from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic


from polls.models import Choice, Question

# Create your views here.

def home(request):

    return render(request, "mysite/index.html")
