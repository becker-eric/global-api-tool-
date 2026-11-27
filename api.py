import json
import urllib.request
import urllib.parse


def fetch_data(url):
    try:
        request = urllib.request.urlopen(url)
        raw = request.read().decode("utf-8")
        return json.loads(raw)
    except Exception:
        print("Error: API call failed.")
        return None


def get_timezone(city, country_code, save_sample=False):
    encoded = urllib.parse.quote(city)
    url = "https://geocoding-api.open-meteo.com/v1/search?name=" + encoded + "&countryCode=" + country_code.upper() + "&count=1&format=json"
    data = fetch_data(url)
    if data is None or "results" not in data or len(data["results"]) == 0:
        return None
    return data["results"][0]["timezone"]


def get_holidays(country_code, year, save_sample=False):
    url = "https://date.nager.at/api/v3/PublicHolidays/" + str(year) + "/" + country_code.upper()
    data = fetch_data(url)
    if data is None:
        return []
    holidays = []
    i = 0
    while i < len(data):
        holidays.append({"date": data[i]["date"], "name": data[i]["name"]})
        i = i + 1
    return holidays