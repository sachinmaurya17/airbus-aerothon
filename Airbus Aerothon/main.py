from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import requests

# Function to get data from Aviation Stack API
aviationstack_api_key = '8a9ab04dd5ea5fa7a523275964e456a3'

def get_aviationstack_data(api_key):
    url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

aviation_data = get_aviationstack_data(aviationstack_api_key)
# Converting aviation data to DataFrame
aviation_df = pd.json_normalize(aviation_data)
aviation_df.to_excel('flight_health.xlsx', index=False)

# Load Excel data
df = pd.read_excel("flight_health.xlsx")

# Fetching weather around the destination
weather_api_key = '27c6cd99506a100f0db1d82f142b9739'

def get_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def identify_scenarios(weather_data):
    scenarios = []
    if 'weather' in weather_data and weather_data['weather']:
        if weather_data['weather'][0]['main'] in ['Rain', 'Snow', 'Fog']:
            scenarios.append('Adverse weather condition')
        else:
            scenarios.append("Moderate Weather")
    else:
        scenarios.append("Weather data not available")

    if 'visibility' in weather_data and 'main' in weather_data:
        if weather_data['visibility'] < 1000:
            scenarios.append('Low visibility')
        else:
            scenarios.append("Path visible")
    else:
        scenarios.append("Visibility data not available")

    return scenarios

def validate_inputs(flight_no, departure_airport, arrival_airport):
    if flight_no not in df['flight.number'].values:
        display_error("Invalid flight number")
        return False
    if departure_airport not in df['departure.airport'].values:
        display_error("Invalid source airport")
        return False
    if arrival_airport not in df['arrival.airport'].values:
        display_error("Invalid destination airport")
        return False
    return True

def button_action():
    flight_no = flightNumber.get()
    departure_airport = departureAirport.get()
    arrival_airport = arrivalAirport.get()
    
    if flight_no and departure_airport and arrival_airport:
        if validate_inputs(flight_no, departure_airport, arrival_airport):
            load_second_view((departure_airport, arrival_airport), flight_no)
    else:
        display_error("Please enter all details")

def check_weather():
    f_no = flightNumber.get()
    departure_airport = departureAirport.get()
    arrival_airport = arrivalAirport.get()
    load_weather_view(departure_airport, arrival_airport, f_no)

def display_error(message):
    error_window = Toplevel(root)
    error_window.title("Error")
    Label(error_window, text=message, font="timesnewroman 16 bold", fg="red").pack(pady=20, padx=20)
    Button(error_window, text="OK", command=error_window.destroy, font="timesnewroman 14 bold").pack(pady=10)

def load_second_view(flight_data, flight_no):
    source, destination = flight_data

    for widget in root.winfo_children():
        widget.destroy()

    bgimg = Image.open("flight.jpg")
    useimg = ImageTk.PhotoImage(bgimg)
    Label(root, image=useimg).place(x=0, y=0)
    root.title("FLY HIGH")
    quote = Label(root, text="We go higher", borderwidth=4, relief=SUNKEN)
    quote.pack(fill=X)

    Label(root, text=f"Flight Number: {flight_no}", font="timesnewroman 18 bold", bg="lightgray").pack(pady=10)
    Label(root, text=f"From: {source}", font="timesnewroman 18 bold", bg="lightgray").pack(pady=10)
    Label(root, text=f"To: {destination}", font="timesnewroman 18 bold", bg="lightgray").pack(pady=10)

    b1 = Button(root, bg="lightgray", pady=10, text="Check Weather", fg="black", font="timesnewroman 16 bold", command=check_weather)
    b1.pack(side=LEFT, padx=80, pady=20)

    b2 = Button(root, bg="lightgray", pady=10, text="See Route", fg="black", font="timesnewroman 16 bold", command=load_route_view)
    b2.pack(side=LEFT, padx=60, pady=20)

    b3 = Button(root, bg="lightgray", pady=10, text="Check Health", fg="black", font="timesnewroman 16 bold", command=check_flight_health)
    b3.pack(side=RIGHT, padx=80, pady=20)

    root.image = useimg

def load_weather_view(source, destination, num):
    for widget in root.winfo_children():
        widget.destroy()

    bgimg = Image.open("flight.jpg")
    useimg = ImageTk.PhotoImage(bgimg)
    Label(root, image=useimg).place(x=0, y=0)
    root.title("FLY HIGH")
    quote = Label(root, text="We go higher", borderwidth=4, relief=SUNKEN)
    quote.pack(fill=X)

    Button(root, text="Go Back", font="timesnewroman 18 bold", fg="black", command=lambda: load_second_view((source, destination), num)).pack(side=TOP, anchor=NW, pady=10, padx=20)

    weather_data_source = get_weather_data(weather_api_key, city=source)
    weather_data_dest = get_weather_data(weather_api_key, city=destination)

    scenarios_source = identify_scenarios(weather_data_source)
    scenarios_dest = identify_scenarios(weather_data_dest)

    source_frame = Frame(root, bg="lightgray")
    source_frame.pack(side=LEFT, fill=Y, padx=30, pady=120)
    Label(source_frame, text=f"{source}", font="timesnewroman 16 bold underline", bg="lightgray").pack(pady=10)
    Label(source_frame, text=f"Temperature: {weather_data_source['main']['temp']}°C", font="timesnewroman 14 bold", bg="lightgray").pack(pady=5)
    Label(source_frame, text=f"Visibility: {weather_data_source['visibility']} m", font="timesnewroman 14 bold", bg="lightgray").pack(pady=5)
    Label(source_frame, text=f"Humidity: {weather_data_source['main']['humidity']}%", font="timesnewroman 14 bold", bg="lightgray").pack(pady=5)
    Label(source_frame, text=f"{', '.join(scenarios_source)}", font="timesnewroman 14 bold", bg="lightgray").pack(pady=10)

    dest_frame = Frame(root, bg="lightgray")
    dest_frame.pack(side=RIGHT, fill=Y, padx=30, pady=120)
    Label(dest_frame, text=f"{destination}", font="timesnewroman 16 bold underline", bg="lightgray").pack(pady=10)
    Label(dest_frame, text=f"Temperature: {weather_data_dest['main']['temp']}°C", font="timesnewroman 14 bold", bg="lightgray").pack(pady=5)
    Label(dest_frame, text=f"Visibility: {weather_data_dest['visibility']} m", font="timesnewroman 14 bold", bg="lightgray").pack(pady=5)
    Label(dest_frame, text=f"Humidity: {weather_data_dest['main']['humidity']}%", font="timesnewroman 14 bold", bg="lightgray").pack(pady=5)
    Label(dest_frame, text=f"{', '.join(scenarios_dest)}", font="timesnewroman 14 bold", bg="lightgray").pack(pady=10)

    root.image = useimg

def check_flight_health():
    f_no = flightNumber.get()
    departure_airport = departureAirport.get()
    arrival_airport = arrivalAirport.get()
    load_health_view(departure_airport, arrival_airport, f_no)
    
    
    
    
    
    
    
      
    
def load_health_view(source, destination, num):
    for widget in root.winfo_children():
        widget.destroy()

    bgimg = Image.open("flight.jpg")
    useimg = ImageTk.PhotoImage(bgimg)
    Label(root, image=useimg).place(x=0, y=0)
    root.title("FLY HIGH")
    quote = Label(root, text="We go higher", borderwidth=4, relief=SUNKEN)
    quote.pack(fill=X)

    Button(root, text="Go Back", font="timesnewroman 18 bold", fg="black", command=lambda: load_second_view((source, destination), num)).pack(side=TOP, anchor=NW, pady=10, padx=20)

    # Simulate retrieving health data (this should be replaced with actual data retrieval)
    health_data = {
        "maintenance_status": "All checks completed",
        "engine_hours": 3200,
        "engine_cycles": 1500,
        "autopilot_status": "Operational",
        "navigation_systems": "Operational",
        "hydraulic_systems": "Operational",
        "electrical_systems": "Operational",
        "environmental_control": "Operational",
        "fdr_status": "Operational",
        "cvr_status": "Operational",
        "weather_preparedness": "Good",
        "pilot_training": "Up to date",
        "crew_fatigue": "None",
        "weight_balance": "Within limits",
        "cargo_securement": "All secure",
        "regulatory_compliance": "Compliant",
    }

    health_frame = Frame(root, bg="lightgray")
    health_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

    canvas = Canvas(health_frame, bg="lightgray")
    scrollbar = Scrollbar(health_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="lightgray")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    Label(scrollable_frame, text="Flight Health Status", font="timesnewroman 16 bold underline", bg="lightgray").pack(pady=10, padx=235)

    for key, value in health_data.items():
        Label(scrollable_frame, text=f"{key.replace('_', ' ').title()}: {value}", font="timesnewroman 14 bold", bg="lightgray").pack(pady=5, padx=220)

    root.image = useimg

# creating GUI
root = Tk()
root.geometry("900x600")
root.maxsize(900, 600)
root.minsize(900, 600)
bgimg = Image.open("flight.jpg")
useimg = ImageTk.PhotoImage(bgimg)
Label(root, image=useimg).place(x=0, y=0)
root.title("FLY HIGH")
quote = Label(root, text="We go higher", borderwidth=4, relief=SUNKEN)
quote.pack(fill=X)

f1 = Frame(root)
f1.pack(pady=50)

flightNumber = IntVar()
departureAirport = StringVar()
arrivalAirport = StringVar()

airports = df['departure.airport'].unique().tolist() 
airports += df['arrival.airport'].unique().tolist()
airports = list(set(airports))  # Remove duplicates

Label(f1, text="Flight Number", font="timesnewroman 16 bold", pady=10).grid(row=0, column=0, padx=10)
Entry(f1, textvariable=flightNumber, width=30, font="timesnewroman 20 bold", borderwidth=4, relief=SUNKEN).grid(row=0, column=1, padx=10)

Label(f1, text="Departure Airport", font="timesnewroman 16 bold", pady=10).grid(row=1, column=0, padx=10)
departure_combobox = ttk.Combobox(f1, textvariable=departureAirport, values=airports, width=28, font="timesnewroman 20 bold")
departure_combobox.grid(row=1, column=1, padx=10)
departure_combobox.bind('<KeyRelease>', lambda event: update_combobox(event, departure_combobox, airports))

Label(f1, text="Arrival Airport", font="timesnewroman 16 bold", pady=10).grid(row=2, column=0, padx=10)
arrival_combobox = ttk.Combobox(f1, textvariable=arrivalAirport, values=airports, width=28, font="timesnewroman 20 bold")
arrival_combobox.grid(row=2, column=1, padx=10)
arrival_combobox.bind('<KeyRelease>', lambda event: update_combobox(event, arrival_combobox, airports))

Button(root, text="Submit", font="timesnewroman 18 bold", padx=15, pady=10, command=button_action).pack(pady=20)

def update_combobox(event, combobox, options):
    value = event.widget.get()
    if value == '':
        combobox['values'] = options
    else:
        filtered_values = [option for option in options if value.lower() in option.lower()]
        combobox['values'] = filtered_values
        combobox.event_generate('<Down>')  # Open the dropdown list

root.image = useimg
root.mainloop()