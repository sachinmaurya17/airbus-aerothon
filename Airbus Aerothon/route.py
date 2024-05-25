import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox
import folium
from geopy.geocoders import Nominatim
from selenium import webdriver
from PIL import Image, ImageTk
import os
import time

# Function to load flight data from Excel
def load_flight_data(filepath):
    df = pd.read_excel(filepath)
    return df

# Function to find routes between two airports
def find_routes(df, source, destination):
    routes = df[(df['departure.iata'] == source) & (df['arrival.iata'] == destination)]
    return routes

# Function to display the map in the main Tkinter window
def display_map_image(map_image_path):
    map_image = Image.open(map_image_path)
    map_image = map_image.resize((600, 400), Image.Resampling.LANCZOS)
    map_image = ImageTk.PhotoImage(map_image)

    if hasattr(display_map_image, 'label'):
        display_map_image.label.configure(image=map_image)
        display_map_image.label.image = map_image  # Keep a reference to avoid garbage collection
    else:
        display_map_image.label = Label(root, image=map_image)
        display_map_image.label.image = map_image  # Keep a reference to avoid garbage collection
        display_map_image.label.pack()

def show_map(routes):
    if not routes.empty:
        geolocator = Nominatim(user_agent="flight_route")
        departure_location = geolocator.geocode("Naha Airport, Okinawa")
        arrival_location = geolocator.geocode("Fukuoka Airport, Fukuoka")

        if departure_location and arrival_location:
            # Create map centered on departure airport
            m = folium.Map(location=[(departure_location.latitude + arrival_location.latitude) / 2,
                                     (departure_location.longitude + arrival_location.longitude) / 2], zoom_start=6)

            # Add markers
            folium.Marker([departure_location.latitude, departure_location.longitude], tooltip='Naha Airport', icon=folium.Icon(color='green')).add_to(m)
            folium.Marker([arrival_location.latitude, arrival_location.longitude], tooltip='Fukuoka Airport', icon=folium.Icon(color='red')).add_to(m)

            # Add route
            folium.PolyLine([(departure_location.latitude, departure_location.longitude), 
                             (arrival_location.latitude, arrival_location.longitude)], color="blue", weight=2.5, opacity=1).add_to(m)

            # Save map to HTML file
            map_html_path = os.path.abspath('flight_route_map.html')
            m.save(map_html_path)

            # Convert HTML to image using selenium
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is in your PATH
            driver.get(f"file:///{map_html_path}")
            time.sleep(2)  # Give it some time to fully load the page

            map_png_path = os.path.abspath('flight_route_map.png')
            driver.save_screenshot(map_png_path)
            driver.quit()

            # Display the image on the GUI
            display_map_image(map_png_path)
        else:
            messagebox.showerror("Error", "Unable to find geolocation for the given airports.")
    else:
        messagebox.showinfo("No Routes", "No direct routes available to show on map.")

def search_routes():
    source = departureAirport.get()
    destination = arrivalAirport.get()
    
    if source and destination:
        routes = find_routes(df, source, destination)
        show_map(routes)
    else:
        messagebox.showerror("Input Error", "Please enter both source and destination airports.")

# Create GUI
root = Tk()
root.geometry("600x600")
root.title("Flight Route Finder")

# Load flight data
df = load_flight_data('flight_health.xlsx')

# Define known airports
airports = ["OKA", "FUK"]

# GUI Elements
Label(root, text="Departure Airport", font="timesnewroman 16 bold", pady=10).pack()
departureAirport = StringVar(value="OKA")
departure_combobox = ttk.Combobox(root, textvariable=departureAirport, values=airports, width=28, font="timesnewroman 14")
departure_combobox.pack(pady=10)

Label(root, text="Arrival Airport", font="timesnewroman 16 bold", pady=10).pack()
arrivalAirport = StringVar(value="FUK")
arrival_combobox = ttk.Combobox(root, textvariable=arrivalAirport, values=airports, width=28, font="timesnewroman 14")
arrival_combobox.pack(pady=10)

Button(root, text="Show Route", font="timesnewroman 14 bold", command=search_routes).pack(pady=20)

root.mainloop()
