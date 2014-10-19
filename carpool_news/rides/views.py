from carpool_news.settings import NEWEST_RIDES
from django.shortcuts import render
from rides.models import Ride, Route


def index(request):
    # Return full list of routes
    routes = Route.objects.order_by('origin', 'destination')
    newest_rides = Ride.objects.order_by('-id')[:NEWEST_RIDES]
    return render(request, 'index.html', {
        'routes': routes,
        'newest_rides': newest_rides,
    })
