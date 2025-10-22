import datetime
import os

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route("/")
def index():
    city = "New Delhi"
    temp = 25
    description = "Clear Sky"
    day = datetime.date.today()
    return render_template(
        "index.html", city=city, temp=temp, description=description, day=day
    )


@app.route("/pred", methods=["GET", "POST"])
def pred():
    # Get city from user input
    city = request.form["city"] if request.method == "POST" else "New Delhi"

    # API request to get weather data
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    PARAMS = {"units": "metric"}
    data = requests.get(url, params=PARAMS).json()

    # Check if data is available
    if "main" not in data:
        flash(
            "Weather information for the selected city is not available. Please enter a valid city name.",
            "error",
        )
        return redirect(url_for("index"))

    try:
        # Extracting weather details
        description = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        max_temp = data["main"]["temp_max"]
        min_temp = data["main"]["temp_min"]
        pressure = data["main"]["pressure"]
        precipitation = data.get("rain", 0)
        cloudiness = data["clouds"]["all"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        # Check for hot weather conditions
        hot_alert = (
            "(Alert) It is hot today! Consider wearing light clothes and staying hydrated."
            if temp >= 40
            else None
        )

        # Check for cold weather conditions
        cold_alert = (
            "(Alert) It is cold today! Don't forget to bundle up."
            if temp <= 10
            else None
        )

        # Construct the weather report message
        report_message = (
            f"Weather report for {city}:\n"
            f"Temperature: {temp}°C\nDescription: {description}\nHumidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\nMax Temperature: {max_temp}°C\nMin Temperature: {min_temp}°C\n"
            f"Pressure: {pressure} hPa\nPrecipitation: {precipitation} mm\nCloudiness: {cloudiness}%\n"
            f"Sunrise: {sunrise}\nSunset: {sunset}\n"
        )

        if hot_alert:
            report_message += f"{hot_alert}\n"
        if cold_alert:
            report_message += f"{cold_alert}\n"

        # Send report message (this function can be called as needed)
        # send_report_message(report_message)

    except KeyError:
        flash(
            "Error retrieving weather information for the selected city. Please try again.",
            "error",
        )
        return redirect(url_for("index"))

    day = datetime.date.today()

    # API request to get an image
    API_KEY = os.getenv("GOOGLE_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = "image"
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
    city_data = requests.get(city_url).json()

    # Extract image URL from search results
    search_items = city_data.get("items")
    image_url = (
        search_items[0]["link"]
        if search_items and len(search_items) > 0
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


# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")


def send_report_message(message):
    # Send SMS
    client.messages.create(to="+919347160789", from_=twilio_phone_number, body=message)

    # Send WhatsApp message
    client.messages.create(
        from_=twilio_phone_number, body=message, to="receiver number with +"
    )


if __name__ == "__main__":
    app.run(debug=True)
