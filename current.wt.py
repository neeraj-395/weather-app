import json
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from tkintermapview import TkinterMapView as MapView
from geopy.geocoders import Nominatim

class Current_Weather(tk.Tk):
    ''' API CREDENTIALS '''
    # api_current (str): The API endpoint URL for fetching current weather data.
    api_current = "https://api.weatherapi.com/v1/current.json"
    # payload (dict): The payload containing API credentials and additional parameters for weather data retrieval.
    payload = {'key': "a78578373e714abbabf51022241205", 'aqi': "yes"}

    def __init__(self):
        ''' Initialize the Current_Weather class. '''
        super().__init__()

        # geolocator (Nominatim): An Nominatim Object used to collect city location data
        self.geolocator = Nominatim(user_agent="Current_Weather")
        
        # weather_data (dict): A dictionary to store weather data, initialized with default values.
        self.weather_data = {"Temperature": "N/A", "Humidity": "N/A"}
        # aqi_data (dict): A dictionary to store air quality index data, initialized with default values.
        self.aqi_data = {"PM2.5": "N/A", "PM10": "N/A"}

        # main_frame (ttk.Frame): The main frame of the application window.
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # map_frame (ttk.Frame): The frame to contain the map view.
        self.map_frame = ttk.Frame(self.main_frame)
        self.map_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # weather_frame (ttk.Frame): The frame to contain weather and air quality index information.
        self.weather_frame = ttk.Frame(self.main_frame)
        self.weather_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        # city_label (ttk.Label): The label to prompt the user to enter city/state information.
        self.city_label = ttk.Label(self.weather_frame, text="Enter City/State:", font=("Serif", 12), justify="center")
        self.city_label.pack(pady=10)
        
        # city_entry (ttk.Entry): The entry widget for user input of city/state information.
        self.city_entry = ttk.Entry(self.weather_frame, justify="center")
        self.city_entry.insert(0, "India")
        self.city_entry.pack(pady=5)

        # search_button (ttk.Button): The button to trigger data retrieval based on user input.
        self.search_button = ttk.Button(self.weather_frame, text="Search", command=self.update_data)
        self.search_button.pack(pady=5)

        '''
         * weather_label (ttk.Label): The label to indicate the weather data section.
         * weather_table (ttk.Treeview): The table to display weather data.
         * aqi_label (ttk.Label): The label to indicate the air quality index data section.
         * aqi_table (ttk.Treeview): The table to display air quality index data.
        '''
        self.weather_label, self.weather_table = self.create_table("Weather")
        self.aqi_label, self.aqi_table = self.create_table("Air Quality Index")

        # map_view (MapView): The map view widget to display geographical information.
        self.map_view = MapView(self.map_frame, width=500, height=500, corner_radius=20)
        self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
        self.map_view.pack(side=tk.RIGHT, padx=20, pady=20)

    def create_table(self, label_text: str) -> tuple[ttk.Label, ttk.Treeview]:
        # create temporary label using Label constructor
        temp_label = ttk.Label(self.weather_frame, text=label_text, font=("Serif", 12), justify="center")
        temp_label.pack(pady=5)
        # create temporary table using Treeview constructor
        temp_table = ttk.Treeview(self.weather_frame, columns=('Parameter','Value'), show="headings", height=8)
        temp_table.heading("Parameter",text="Parameter", anchor="center")
        temp_table.heading("Value", text="Value", anchor="center")
        temp_table.column("Parameter", width=100, anchor="center")
        temp_table.column("Value", width=100, anchor="center")
        temp_table.pack(padx=10, pady=5)
        # return the tuples label and table
        return temp_label, temp_table

    def update_data(self):
        # Get location of input city
        try:
            loc = self.geolocator.geocode(self.city_entry.get()).raw # type: ignore
        except:
            messagebox.showinfo("City Not Found","Please enter a valid city name.")
            return
        
        # Bounding box format: [south, north, west, east]
        bbox = loc['boundingbox']
        ptl = (float(bbox[1]), float(bbox[2]))
        pbr = (float(bbox[0]), float(bbox[3]))
        self.map_view.fit_bounding_box(ptl, pbr)
        
        self.payload.update({'q': f"{loc['lat']},{loc['lon']}"})
        data = self.fetch_data(self.api_current, self.payload)

        self.weather_data["Temperature"] = data['current']['temp_c'] if data else "N/A"
        self.weather_data["Humidity"] = data['current']['humidity'] if data else "N/A"

        self.aqi_data['PM2.5'] = data['current']['air_quality']['pm2_5'] if data else "N/A"
        self.aqi_data['PM10']  = data['current']['air_quality']['pm10'] if data else "N/A"

        self.update_info(self.weather_table, self.weather_data)
        self.update_info(self.aqi_table, self.aqi_data)

    def fetch_data(self, apiUrl: str, payload: dict[str,str]) -> dict | None:
        try:
            response = requests.get(apiUrl, params=payload)
            # This is our check to ensure a successful web connection
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                messagebox.showinfo("Data Error", "The requested data was not found.")
                return None
        except:
            messagebox.showinfo("Connection Error", "Please check your internet connection and try again.")
            return None

    def update_info(self, table: ttk.Treeview, data: dict) -> None:
        table.delete(*table.get_children())
        for param, value in data.items():
            table.insert('', tk.END, values=(param, value))
        

if __name__ == "__main__":
    app = Current_Weather()
    app.title("Weather Analyzer App")
    app.geometry("800x600")
    app.resizable(False, False) 
    app.protocol("WM_DELETE_WINDOW", app.quit())
    app.after_idle(app.update_data)
    app.mainloop()