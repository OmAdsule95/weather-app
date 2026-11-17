
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = None

    if request.method == "POST":
        city = request.form["city"]

        try:
            
            response = requests.get(url, params={
                "name": city,
                "count": 1
            }, timeout=10)

            data = response.json()

            if "results" in data:
                location = data["results"][0]

                latitude = location["latitude"]
                longitude = location["longitude"]

                

                response = requests.get(url, params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
                }, timeout=10)

                result = response.json()["current"]

                weather = {
                    "city": location["name"],
                    "temperature": result["temperature_2m"],
                    "humidity": result["relative_humidity_2m"],
                    "wind": result["wind_speed_10m"]
                }

            else:
                error = "City not found!"

        except (requests.RequestException, KeyError, ValueError):
            error = "Unable to get weather information!"

    return render_template("index.html", weather=weather, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
