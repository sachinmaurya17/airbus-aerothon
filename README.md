FLY HIGH - Flight Information System
FLY HIGH is a flight information system built using Python and Tkinter GUI toolkit. It provides real-time flight data, weather information, and flight health status.

Features
Flight Information: Enter flight number, departure, and arrival airports to get detailed information about the flight.
Weather Information: Check the weather conditions at the departure and arrival airports.
Flight Health Status: View the health status of the flight including maintenance status, engine hours, autopilot status, and more.
Installation
Install the required packages:

bash

pip install -r requirements.txt

Run the application:

python main.py


Usage
Enter the flight number, departure airport, and arrival airport in the respective fields.
Click on the "Submit" button to view flight details.
Optionally, click on the "Check Weather" button to view weather information.
To check the health status of the flight, click on the "Check Health" button.
Dependencies
Tkinter: Python's de-facto standard GUI (Graphical User Interface) package.
Pandas: Data manipulation and analysis library.
Requests: HTTP library for making API requests.
Pillow (PIL): Python Imaging Library for working with images.
API Keys
Aviation Stack API Key: Obtain your API key from Aviation Stack to fetch real-time flight data.
OpenWeatherMap API Key: Get your API key from OpenWeatherMap to retrieve weather data
