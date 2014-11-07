import math
from carpool_news.settings import NEWEST_RIDES, RIDES_PER_PAGE
from django.shortcuts import render
from rides.models import Ride, Route, Location
from rides.forms import SearchForm


def index(request):
    if request.GET.items():
        # Create from GET params if available
        form = SearchForm(request.GET)
        # Do the search according to these params
        rides = Ride.objects.filter(
            routes__origin=form.origin_value,
            routes__destination=form.destination_value,
            is_looking_for=form.is_looking_for_value,
            is_expired=False)
        search_done = True
    else:
        # Populate with initial values otherwise
        form = SearchForm()
        # Display few newest ads
        rides = Ride.objects.filter(
            is_expired=False).order_by('-id')[:NEWEST_RIDES]
        search_done = False

    return render(request, 'rides/index.html', {
        'search_done': search_done,
        'form': form,
        'rides': rides,
        'rides_per_page': RIDES_PER_PAGE,
        'ride_pages': math.ceil(float(len(rides)) / RIDES_PER_PAGE),
    })
