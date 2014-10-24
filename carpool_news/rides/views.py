from carpool_news.settings import NEWEST_RIDES, RIDES_PER_PAGE
from django.shortcuts import render
from rides.models import Ride, Route
import math


def index(request):
    # Search parameters
    origin = request.GET.get('from')
    destination = request.GET.get('to')
    looking_for_str = request.GET.get('looking-for')

    # Convert to boolean
    if looking_for_str == 'True':
        looking_for = True
    elif looking_for_str == 'False':
        looking_for = False
    else:
        looking_for = None

    if origin and destination:
        search_done = True
        # Do the search
        rides = list(set([
            ride
            for route in Route.objects.filter(
                origin=origin,
                destination=destination)
            for ride in route.ride_set.filter(
                is_looking_for=not looking_for)
        ]))
    else:
        search_done = False
        # Display few newest rides
        rides = Ride.objects.order_by('-id')[:NEWEST_RIDES]
        origin = ""
        destination = ""

    city_options = Route.unique_cities()
    return render(request, 'rides/index.html', {
        'search_done': search_done,
        'selected_origin': origin,
        'selected_destination': destination,
        'selected_looking_for': looking_for,
        'city_options': city_options,
        'rides': rides,
        'rides_per_page': RIDES_PER_PAGE,
        'ride_pages': math.ceil(float(len(rides)) / RIDES_PER_PAGE),
    })
