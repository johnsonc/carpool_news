from carpool_news.settings import NEWEST_RIDES, RIDES_PER_PAGE
from django.shortcuts import render
from rides.models import Ride, Route, Location
import math


def index(request):
    # Search parameters
    origin = Location.get_by_name(request.GET.get('from'))
    destination = Location.get_by_name(request.GET.get('to'))
    looking_for_str = request.GET.get('looking-for')

    # Convert to boolean
    if looking_for_str == 'True':
        looking_for = True
    elif looking_for_str == 'False':
        looking_for = False
    else:
        looking_for = None

    if origin is not None and destination is not None:
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
        origin_name, destination_name = origin.name, destination.name
    else:
        search_done = False
        # Display few newest rides
        rides = Ride.objects.order_by('-id')[:NEWEST_RIDES]
        origin_name = ""
        destination_name = ""

    city_options = Location.objects.all()
    return render(request, 'rides/index.html', {
        'search_done': search_done,
        'selected_origin': origin_name,
        'selected_destination': destination_name,
        'selected_looking_for': looking_for,
        'city_options': city_options,
        'rides': rides,
        'rides_per_page': RIDES_PER_PAGE,
        'ride_pages': math.ceil(float(len(rides)) / RIDES_PER_PAGE),
    })
