from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from amadeus import Client, ResponseError
from amadeus.client.decorator import Decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
import os
from datetime import datetime

from .models import Airport, Trip, Hotel, Flight, User

# Create your views here.
amadeus = Client(
    client_id=os.environ.get("AMADEUS_CLIENT_ID"),
    client_secret=os.environ.get("AMADEUS_CLIENT_SECRET")
)


def home(request):
    # response = amadeus.get('/v1/shopping/flight-destinations', origin='LAX')
# #     print(response.data)
#     for r in response.data:
#         a = r['price']['total']
#         a = float(a)
#         if a < 300:
#             print(
#                 f"""FROM LAX 
#                 \nDestination: {r['destination']} 
#                 \tprice: {a} 
#                 \t departure date: {r['departureDate']}
#                   \t return date: {r['returnDate']}"""
#                   )
    return render(request, 'home.html', 
    # { "flights": response.data}
    )


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid credentials - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def destinations(request):
    origin = request.POST.get('origin')
    d_date = request.POST.get('d_date')
    budget = float(request.POST.get('budget'))

    if request.user.is_authenticated:
        trip = Trip(budget=budget, user=request.user, origin=origin)
        trip.save()
    else:
        print('no user')

    search_list = amadeus.shopping.flight_destinations.get(
        origin=origin,
        departureDate=d_date
        ).data

    destinations = []
    for destination in search_list:
        d_price = float(destination['price']['total'])
        if d_price <= budget/2:
            destinations.append(destination)

    return render(request, 'destinations/search.html', {'destinations': destinations, 'budget': budget, 'origin': origin, 'departure_date':d_date, "trip": trip})

def hotel_search(request, trip_id, airport_code):
    budget = float(request.POST.get('budget'))
    trip = Trip.objects.get(id=trip_id)
    hotel_search = amadeus.shopping.hotel_offers.get(cityCode=airport_code).data
# print(json.dumps(hotel_search, indent=2))
    hotels = []
    for hotel in hotel_search:
        h_price = float(hotel['offers'][0]['price']['total'])
        if h_price <= budget/3:
            hotels.append(hotel) 
    return render(request, 'hotels/search.html', {'hotels' : hotels, 'trip': trip, 'airport_code': airport_code})

def flight_search(request, trip_id, airport_code):
    budget = float(request.POST.get('budget'))
    origin = request.POST.get('origin')
    departure_date = request.POST.get('departure_date') or request.POST.get('return_date')
    trip = Trip.objects.get(id=trip_id)

    # if return_date:
    #     return_date = datetime.strptime(departure_date, '%B %d %Y').strftime('%Y-%m-%d')
    #     flight_search = amadeus.shopping.flight_offers.get(destination=airport_code, origin=origin, departureDate=return_date).data
    # else:
    flight_search = amadeus.shopping.flight_offers.get(destination=airport_code, origin=origin, departureDate=departure_date).data
    
    flights = []
    for flight in flight_search:
        f_price = float(flight['offerItems'][0]['price']['total'])
        f_origin = flight['offerItems'][0]['services'][0]['segments'][0]['flightSegment']['departure']['iataCode']
        f_destination = flight['offerItems'][0]['services'][0]['segments'][0]['flightSegment']['arrival']['iataCode']
        if f_price <= budget/3 and f_origin == origin and f_destination == airport_code:
            flights.append(flight)
    

    return render(request, 'flights/search.html', {'flights': flights, 'trip': trip, 'departure_date': departure_date, 'airport_code': airport_code})

def flight_add(request, trip_id, airport_code):
    price = request.POST.get('price')
    trip = Trip.objects.get(id=trip_id)
    origin = request.POST.get('origin')
    destination = request.POST.get('destination')
    departure_date = request.POST.get('departure_date')
    airport_code = airport_code
        
    current_flight = Flight.objects.create(
        departure_date = departure_date,
        destination = destination,
        price = price,
        origin = origin,
        trip = trip,
        )
    if trip.origin == airport_code:
        return redirect(f'/trips/{trip.id}/{airport_code}')
    else: 
        return redirect(f'/trips/{trip.id}/{origin}')
    # return render(request, 'trip.html', {'current_flight': current_flight})

def hotel_add(request, trip_id, airport_code):
    price = request.POST.get('price')
    name = request.POST.get('name')
    check_out = request.POST.get('check_out')
    check_in = request.POST.get('check_in')
    street = request.POST.get('street')
    city = request.POST.get('city')
    trip = Trip.objects.get(id=trip_id)
    origin = airport_code

    current_hotel = Hotel.objects.create(
        name = name,
        check_out = check_out,
        check_in = check_in, 
        address = street + city,
        price = price,
        trip = trip
        )

    print(current_hotel.trip)
    
    return redirect(f'/trips/{trip.id}/{origin}')

class CreateTrip(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['name', 'budget', 'origin', 'departure_date', 'return_date']
    def form_valid(self, form):
        form.instance.user = self.request.user    # Let the CreateView do its job as usual
        return super().form_valid(form)

def trips_detail(request, trip_id, airport_code):
    trip = Trip.objects.get(id=trip_id)
    print(trip)
    origin = airport_code
   
    try:
        depart_flight = Flight.objects.get(trip=trip, origin=origin)
        print('true')
    except:
        depart_flight = None
        print('false')

    try: 
        return_flight = Flight.objects.get(trip=trip, destination=origin)
        print('true')
    except:
        return_flight = None
        print('false')

    try:
        hotel = Hotel.objects.get(trip=trip)
        print('true')
    except:
        hotel = None
        print('false')
    
    return render(request, 'trips/detail.html', {
        'trip': trip,
        'hotel': hotel,
        'depart_flight': depart_flight, 
        'return_flight': return_flight,
    })

class TripList(ListView):
    model = Trip

class TripDelete(LoginRequiredMixin, DeleteView):
    model = Trip
    success_url = '/trips/'

class TripEdit(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = ['name', 'budget']
    # success_url = '/trips/'

def SaveTrip(request):
    form = request.POST
    print(form)
    # new_trip = form.save(commit=False)
    # Trip.flight = request.POST.get('flight','')
    # Trip.budget = 1000
    # Trip.name = request.POST.get('name')
    # Trip.user = 'meisam'

    # Trip.save()
    # return redirect('destination_search')