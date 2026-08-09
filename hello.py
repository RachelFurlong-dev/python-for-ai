import requests

def get_weather(latitude, longitude):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    )

    data = response.json()

    print(data)

    return data["current"]["temperature_2m"]

paris_temp = get_weather(48.85, 2.35)

print(paris_temp)