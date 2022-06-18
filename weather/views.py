import urllib.request
from django.shortcuts import render
import json


# Create your views here.
def index(request):
    if request.method == "POST":
        city = request.POST['city']
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=ce4484ccba09ec9eb5c7a0d33b1d8d54"
        url = url.replace(" ", "%20")
        res = urllib.request.urlopen(url).read()
        json_res = json.loads(res)
        data = {
            "country_code": str(json_res['sys']['country']),
            "coordinate": str(json_res['coord']['lon']) + ' lon ' + str(json_res['coord']['lat']) + ' lat',
            "description": str(json_res['weather'][0]['description']),
            "temperature": str(json_res['main']['temp']) + ' °F',
            "feels_like": str(json_res['main']['feels_like']) + ' °F',
            "humidity": str(json_res['main']['humidity']) + ' °F'
        }
    else:
        city = ''
        data = ''
    return render(request, "index.html", {"city": city, "data": data})
