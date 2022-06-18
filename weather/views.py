import urllib.request
from django.contrib import messages
from django.shortcuts import render, redirect
import json
from urllib.error import HTTPError
import re


# Create your views here.
def index(request):
    if request.method == "POST":
        try:
            city = request.POST['city']
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

            # Check if no value was entered for city
            if city is '' or regex.search(city) is not None:
                data = {}
                messages.info(request, "Invalid city entered. Please do not enter symbols.")
                return render(request, "index.html", {"city": city, "data": data})

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial" \
                  f"&appid=ce4484ccba09ec9eb5c7a0d33b1d8d54"
            # Replacing spaces in url with '%20' to avoid errors
            url = url.replace(" ", "%20")
            res = urllib.request.urlopen(url).read()
            json_res = json.loads(res)

            # Defining data I want to use from the json response
            data = {
                "country_code": str(json_res['sys']['country']),
                "coordinate": str(json_res['coord']['lon']) + ' lon ' + str(json_res['coord']['lat']) + ' lat',
                "description": str(json_res['weather'][0]['description']),
                "temperature": str(json_res['main']['temp']) + ' °F',
                "feels_like": str(json_res['main']['feels_like']) + ' °F',
                "humidity": str(json_res['main']['humidity']) + ' °F'
            }

        # Catching HTTPError 404 if location was not found
        except HTTPError as err:
            if err.code == 404:
                # Adding error to messages to be displayed on screen
                messages.info(request, "Location not found")
                return redirect('index')
        except TypeError:
            messages.info(request, "String only")
            return redirect('index')

    # Handles index rendering for GET request
    else:
        city = ''
        data = {}

    return render(request, "index.html", {"city": city, "data": data})
