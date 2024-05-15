import json
import pytz
import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkintermapview import TkinterMapView as MapView
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import *
from PIL import Image, ImageTk

class Current_Weather(tk.Tk):
    ''' API CREDENTIALS '''
    api_current = "https://api.weatherapi.com/v1/current.json"
    payload = {'key': "a78578373e714abbabf51022241205", 'aqi': "yes"}

    def __init__(self):
        ''' Initialize the Current_Weather class. '''
        super().__init__()
        
        self.weather_data = {"Temperature": "N/A", "Humidity": "N/A"}
        self.aqi_data = {"PM2.5": "N/A", "PM10": "N/A"}
    
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.map_frame = ttk.Frame(self.main_frame)
        self.map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=(10, 100))

        self.weather_frame = ttk.Frame(self.main_frame)
        self.weather_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(10, 100))

        self.city_label = ttk.Label(self.weather_frame, text="Enter City/State:", font=("Serif", 12), justify="center")
        self.city_label.pack(pady=0)
        
        pil_image = Image.open("pic/aqi.png")
        new_size = (200, 40)
        resized_image = pil_image.resize(new_size, Image.LANCZOS)
        search_image = ImageTk.PhotoImage(resized_image)

        self.myimage = tk.Label(self, image=search_image)
        self.myimage.image = search_image
        self.myimage.place(x=15, y=30)

        self.city_entry = tk.Entry(self, justify="center", fg="white", bg="black", bd=0, highlightthickness=0, insertbackground="white")
        self.city_entry.insert(0, "India")
        self.city_entry.place(x=20, y=40, width=180, height=30)
        self.city_entry.focus()

        try:
            search_icon = Image.open("pic/search_icon.png")
            search_icon = search_icon.resize((40, 40), Image.LANCZOS)
            search_icon_image = ImageTk.PhotoImage(search_icon)
            search_button = tk.Button(self, image=search_icon_image, borderwidth=0, cursor="hand2", bg="black", command=self.update_data)
            search_button.image = search_icon_image
            search_button.place(x=180, y=30.5)
        except Exception as e:
            print("Error:", e)
        
        self.buttons_frame = ttk.Frame(self.weather_frame)
        self.buttons_frame.pack(pady=45)

        self.search_button_1 = ttk.Button(self.buttons_frame, text="Graph 1")
        self.search_button_1.pack(side=LEFT, padx=10)

        self.search_button_2 = ttk.Button(self.buttons_frame, text="Graph 2")
        self.search_button_2.pack(side=LEFT, padx=10)

        self.weather_labels = {}
        self.create_labels()

        self.map_view = MapView(self.map_frame, width=500, height=550, corner_radius=20)
        self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_view.pack(side=tk.RIGHT, padx=20, pady=10)

        #self.create_bottom_frame()

    def create_labels(self):
        pil_image = Image.open("pic/day.jpeg")
        new_size = (200, 200)
        resized_image = pil_image.resize(new_size, Image.LANCZOS)
        weather_image = ImageTk.PhotoImage(resized_image)
        self.weather_image_label = tk.Label(self, image=weather_image)
        self.weather_image_label.image = weather_image
        self.weather_image_label.place(x=19, y=143)

        pil_image_icon = Image.open("pic/weather-icon.png")
        new_size_icon = (100, 80)
        resized_image_icon = pil_image_icon.resize(new_size_icon, Image.LANCZOS)
        weather_icon_image = ImageTk.PhotoImage(resized_image_icon)
        self.weather_icon_label = tk.Label(self, image=weather_icon_image, bg="#F29F05")
        self.weather_icon_label.image = weather_icon_image
        self.weather_icon_label.place(x=30, y=153)

        self.weather_labels["Temperature"] = tk.Label(self, text="Temperature: N/A", font=("serif", 12), fg="black", bg="#F29F05")
        self.weather_labels["Temperature"].place(x=30, y=240)
        self.weather_labels["Humidity"] = tk.Label(self, text="Humidity: N/A", font=("serif", 12), fg="black", bg="#F29F05")
        self.weather_labels["Humidity"].place(x=30, y=260)
        self.weather_labels["Pressure"] = tk.Label(self, text="Pressure: N/A", font=("serif", 12), fg="black", bg="#F29F05")
        self.weather_labels["Pressure"].place(x=30, y=280)
        self.weather_labels["Wind Speed"] = tk.Label(self, text="Wind Speed: N/A", font=("serif", 12), fg="black", bg="#F29F05")
        self.weather_labels["Wind Speed"].place(x=30, y=300)
        self.weather_labels["Description"] = tk.Label(self, text="Description: N/A", font=("serif", 12), fg="black", bg="#F29F05")
        self.weather_labels["Description"].place(x=30, y=320)

        pil_image = Image.open("pic/aqi1.png")
        new_size = (200, 200)
        resized_image = pil_image.resize(new_size, Image.LANCZOS)
        aqi_image = ImageTk.PhotoImage(resized_image)
        self.aqi_image_label = tk.Label(self, image=aqi_image)
        self.aqi_image_label.image = aqi_image
        self.aqi_image_label.place(x=19, y=375)

        self.aqi_labels = {}
        self.aqi_labels["PM10"] = tk.Label(self, text="PM10: N/A", font=("serif", 12), fg="white", bg="#595959")
        self.aqi_labels["PM10"].place(x=30, y=460)
        self.aqi_labels["PM2.5"] = tk.Label(self, text="PM2.5: N/A", font=("serif", 12), fg="white", bg="#595959")
        self.aqi_labels["PM2.5"].place(x=30, y=480)
        self.aqi_labels["Ozone"] = tk.Label(self, text="Ozone: N/A", font=("serif", 12), fg="white", bg="#595959")
        self.aqi_labels["Ozone"].place(x=30, y=500)
        self.aqi_labels["CO"] = tk.Label(self, text="CO: N/A", font=("serif", 12), fg="white", bg="#595959")
        self.aqi_labels["CO"].place(x=30, y=520)
        self.aqi_labels["sulphur"] = tk.Label(self, text="sulphur: N/A", font=("serif", 12), fg="white", bg="#595959")
        self.aqi_labels["sulphur"].place(x=30, y=540)

        self.clock_label = tk.Label(self, text="9:30 pm", font=("serif", 30, 'bold'), fg="black", bg="white")
        self.clock_label.place(x=35, y=390)
    '''
    def create_bottom_frame(self):
        self.bottom_frame = Frame(self, width=800, height=100, bg="#212120")
        self.bottom_frame.pack(side=BOTTOM, fill=X)
    '''
    def update_data(self):
        loc = self.get_location(self.city_entry.get())
        if loc:
            bbox = loc.raw['boundingbox']  # type: ignore
            if bbox:
                ptl = (float(bbox[1]), float(bbox[2]))
                pbr = (float(bbox[0]), float(bbox[3]))
                self.map_view.fit_bounding_box(ptl, pbr)
            
            self.payload.update({'q': f"{loc.latitude},{loc.longitude}"})  # type: ignore
            data = self.fetch_data(self.api_current, self.payload)

            self.weather_data["Temperature"] = data['current']['temp_c'] if data else "N/A"
            self.weather_data["Humidity"] = data['current']['humidity'] if data else "N/A"
            self.weather_data["Pressure"] = data['current']['pressure_mb'] if data else "N/A"
            self.weather_data["Wind Speed"] = data['current']['wind_kph'] if data else "N/A"
            self.weather_data["Description"] = data['current']["condition"]['text'] if data else "N/A"

            self.aqi_data['PM2.5'] = data['current']['air_quality']['pm2_5'] if data else "N/A"
            self.aqi_data['PM10'] = data['current']['air_quality']['pm10'] if data else "N/A"
            self.aqi_data['Ozone'] = data['current']['air_quality']['o3'] if data else "N/A"
            self.aqi_data['CO'] = data['current']['air_quality']['co'] if data else "N/A"
            self.aqi_data['sulphur'] = data['current']['air_quality']['so2'] if data else "N/A"

            self.update_labels()
            self.update_time(loc.latitude, loc.longitude)
        else:
            print("Error: city not found")

    def get_location(self, city: str):
        geolocator = Nominatim(user_agent="WeatherApp")
        return geolocator.geocode(city)

    def fetch_data(self, apiUrl: str, payload: dict) -> dict | None:
        try:
            response = requests.get(apiUrl, params=payload)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                raise Exception("Requested rejected with error code (500).")
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def update_labels(self):
        for key, label in self.weather_labels.items():
            label.config(text=f"{key}: {self.weather_data[key]}")

        for key, label in self.aqi_labels.items():
            label.config(text=f"{key}: {self.aqi_data[key]}")

    def update_time(self, lat, lon):
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        if timezone_str:
            timezone = pytz.timezone(timezone_str)
            local_time = datetime.now(timezone)
            self.clock_label.config(text=local_time.strftime("%I:%M %p"))

if __name__ == "__main__":
    app = Current_Weather()
    app.title("Weather Analyzer App")
    app.configure(bg="#3776ab")
    app.geometry("800x800")
    app.resizable(False, False)
    app.protocol("WM_DELETE_WINDOW", app.quit())
    app.after_idle(app.update_data)
    app.mainloop()
