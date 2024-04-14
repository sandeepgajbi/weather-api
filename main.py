from flask import Flask, render_template, jsonify, request
from datetime import datetime
import logging
import time

app = Flask(__name__)

# Example list of valid stations
VALID_STATIONS = ["10", "15", "20"]

# Configure logger
logging.basicConfig(level=logging.DEBUG)


@app.before_request
def before_request():
    request._start_time = time.time()


@app.after_request
def after_request(response):
    # Log HTTP status code
    app.logger.info(f"HTTP status: {response.status_code}")

    # Calculate time taken to respond
    time_taken = time.time() - getattr(request, '_start_time')
    app.logger.info(f"Time taken to respond: {time_taken:.6f} seconds")

    return response


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def weather_api(station, date):
    try:
        # Log user inputs
        app.logger.info(f"Request: Station={station}, Date={date}")

        # Validate station and date parameters
        if not station or not date:
            app.logger.error("Missing station or date")
            return jsonify({"error": "Station and date parameters are required."}), 400

        if station not in VALID_STATIONS:
            app.logger.error(f"Invalid station: {station}")
            return jsonify({"error": f"Invalid station: {station}"}), 400

        try:
            # Validate date format and check if it's a valid date
            date_obj = datetime.strptime(date, "%Y%m%d")
            if not (1900 <= date_obj.year <= 2100):
                raise ValueError("Invalid year. Year must be between 1900 and 2100.")
        except ValueError as ve:
            app.logger.error(f"Invalid date format: {ve}")
            return jsonify({"error": f"Invalid date format. Date format must be YYYYMMDD."}), 400

        # Fetch weather data from database or external API
        temperature = 23  # Placeholder temperature value

        # Log API output
        app.logger.info(f"Response: Station={station}, Date={date}, Temperature={temperature}")

        # Return weather data as JSON response
        return jsonify({"station": station, "date": date, "temperature": temperature}), 200

    except Exception as e:
        # Log the error
        app.logger.error(f"An unexpected error occurred: {str(e)}")
        # Return error response
        return jsonify({"error": "An unexpected error occurred."}), 500


if __name__ == "__main__":
    # Run Flask app
    app.run(debug=True)
