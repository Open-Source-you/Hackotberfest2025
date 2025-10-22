import datetime

import requests
from flask import Flask, flash, redirect, render_template, request, url_for
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = "alslksdjflksdfjslkdfj"


# flask routes
@app.route("/")
def index():
    # Default values for demonstration, replace with your logic to get actual data
    city = "Burundi"
    temp = 25
    description = "Clear sky"
    day = datetime.date.today()
    return render_template(
        "index.html", city=city, temp=temp, description=description, day=day
    )


@app.route("/pred", methods=["POST"])
def pred():
    # get city name from user (interface html)
    city = request.form["city"] if request.method == "POST" else "Burundi"

    # API request to get weather data
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=here paste your api key shown you in video"
    # {'units': 'metric'}: This line defines a dictionary PARAMS with request parameters. In this case, it specifies that the units
    # for temperature will be returned in metric units (e.g., Celsius).
    PARAMS = {"units": "metric"}
    data = requests.get(url, params=PARAMS).json()

    # Check if weather data is available
    if "main" not in data:
        flash(
            "Weather information for the selected city is not available. Please enter a valid city name.",
            "error",
        )
        return redirect(url_for("index"))
    # Extract weather information from API response
    try:
        # Extracting weather description
        description = data["weather"][0]["description"]
        # Extracting weather icon
        icon = data["weather"][0]["icon"]
        # Extracting temperature
        temp = data["main"]["temp"]
        # Extracting humidity
        humidity = data["main"]["humidity"]
        # Extracting wind speed
        wind_speed = data["wind"]["speed"]
        # Extracting maximum temperature
        max_temp = data["main"]["temp_max"]
        # Extracting minimum temperature
        min_temp = data["main"]["temp_min"]
        # Extracting atmospheric pressure
        pressure = data["main"]["pressure"]
        # Extracting precipitation (rainfall)
        precipitation = data.get("rain", 0)
        # Extracting cloudiness
        cloudiness = data["clouds"]["all"]
        # Extracting sunrise time and converting it to datetime
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        # Extracting sunset time and converting it to datetime
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        # Check for hot weather conditions
        if temp >= 40:
            hot_alert = "(Alert) It is hot today! Consider wearing light clothes and staying hydrated."
        else:
            hot_alert = None

        # Check for cold weather conditions
        if temp <= 10:
            cold_alert = "(Alert) It is cold today! Don't forget to bundle up."
        else:
            cold_alert = None
        # You can add more conditions for other weather parameters (e.g., wind_speed, humidity, etc.)

        # Construct report message with weather values and alerts
        report_message = f"Weather report for {city}:\nTemperature: {temp}°C\nDescription: {description}\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s\nMax Temperature: {max_temp}°C\nMin Temperature: {min_temp}°C\nPressure: {pressure} hPa\nPrecipitation: {precipitation} mm\nCloudiness: {cloudiness}%\nSunrise: {sunrise}\nSunset: {sunset}\n"

        # Append hot weather alert to report message if applicable
        if hot_alert:
            report_message += f"{hot_alert}\n"
        # Append cold weather alert to report message if applicable
        if cold_alert:
            report_message += f"{cold_alert}\n"

        # Send report message
        send_report_message(report_message)

    except KeyError:
        # Handle error if weather information is not available for the selected city
        flash(
            "Error retrieving weather information for the selected city. Please try again.",
            "error",
        )
        return redirect(url_for("index"))

    # getting current time
    day = datetime.date.today()

    # API request to get image URL (for that city)
    API_KEY = "you api key (google search engine as shown video"
    SEARCH_ENGINE_ID = "do here id as shown in video"
    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = "image"
    # Construct URL for Google Custom Search API request to get image URL
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
    # Send API request to Google Custom Search API
    city_data = requests.get(city_url).json()
    # Extract image search results
    search_items = city_data.get("items")
    # Extract image URL if search results are available, otherwise use default image URL
    image_url = (
        search_items[1]["link"]
        if search_items
        else "https://example.com/default_image.jpg"
    )

    # Render HTML template with weather information and image URL
    return render_template(
        "index.html",
        description=description,
        icon=icon,
        temp=temp,
        humidity=humidity,
        wind_speed=wind_speed,
        max_temp=max_temp,
        min_temp=min_temp,
        pressure=pressure,
        precipitation=precipitation,
        cloudiness=cloudiness,
        day=day,
        city=city,
        sunrise=sunrise,
        sunset=sunset,
        hot_alert=hot_alert,
        cold_alert=cold_alert,
        image_url=image_url,
    )


# sending report and alert messages notefications
# Twilio credentials
account_sid = "twilio sid already shown in video"
auth_token = "token "
client = Client(account_sid, auth_token)
twilio_phone_number = "twilio number"


def send_report_message(message):
    # Send SMS
    client.messages.create(
        to="receiver number with +", from_=twilio_phone_number, body=message
    )

    # Send WhatsApp message
    client.messages.create(
        from_=twilio_phone_number, body=message, to="receiver number with +"
    )


if __name__ == "__main__":
    app.run(debug=True)
