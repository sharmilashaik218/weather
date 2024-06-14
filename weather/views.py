from django.shortcuts import *
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f70fec28b5411c57d6adcf8f2531ed4c'

    cities = City.objects.all()
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm()
    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()

        # Print out the city_weather dictionary for debugging
        print(city_weather)

        try:
            weather = {
                'city': city,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
        except KeyError as e:
            print(f"KeyError: {e} for city {city}")
            continue  # Skip this city and move to the next one

        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context)
