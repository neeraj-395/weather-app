import tkinter as tk
from utils.dmf import fetch_data
from tkinter import ttk, messagebox
from geopy.geocoders import Nominatim
from utils.graphs import temperature_graph
from utils.gui import create_card, create_labels
from tkintermapview import TkinterMapView as MapView

''' API CREDENTIALS '''
CURRENT_API = "https://api.weatherapi.com/v1/current.json"
FORECAST_API = "https://api.weatherapi.com/v1/forecast.json"
CURRENT_PAYLOAD = {'key': 'a78578373e714abbabf51022241205','aqi': 'yes'}
FORECAST_PAYLOAD = {'key': 'a78578373e714abbabf51022241205','days':'14','hours':'-1'}

''' API DATA KEY PAIRS'''
WEATHER_KEY_PAIR = {'Temp (°C)': 'temp_c', 'Humidity (%)': 'humidity', 'Pressure (hPa)': 'pressure_mb', 'Wind (m/s)':'wind_kph'}
AQI_KEY_PAIR = {'PM2.5 (μg/m3)':'pm2_5','PM10 (μg/m3)':'pm10','Ozone (μg/m3)':'o3','CO (μg/m3)':'co','Sulphur (μg/m3)':'so2'}

''' HEX CODE FOR CARDS BACKGROUND'''
DAY_BG_HEX = "#F29F05"
NIGHT_BG_HEX = "#890189"
AQI_BG_HEX = "#616161"

class Current_Weather(tk.Tk):
    def __init__(self):
        ''' Initialize the Current_Weather class. '''
        super().__init__()

        self.geoloc = Nominatim(user_agent="Weather_App")
    
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.map_frame = ttk.Frame(self.main_frame)
        self.map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.city_label = ttk.Label(self.control_frame, text="Enter City/State:", font=("serif", 12), justify="center")
        self.city_label.pack(pady=5)

        self.city_entry = tk.Entry(self, justify="center", fg="white", bg="black", insertbackground="white")
        self.city_entry.insert(0, "India")
        self.city_entry.place(x=20, y=40, width=165, height=30)

        self.search_icon = create_card("assets/other/search.png", (30, 24))
        search_button = tk.Button(self, image=self.search_icon, cursor="hand2", bg="black", command=self.update_data) # type: ignore
        search_button.place(x=185, y=40)
        
        self.btn_frame = ttk.Frame(self.control_frame)
        self.btn_frame.pack(pady=60)

        tplot_btn = tk.Button(self.btn_frame, text="T-Plot", bg="black", fg="white", command=self.tplot)
        tplot_btn.pack(side=tk.LEFT, padx=20)

        aplot_btn = tk.Button(self.btn_frame, text="A-Plot", bg="black", fg="white")
        aplot_btn.pack(side=tk.RIGHT)

        self.day_icon = create_card("assets/weather/day.png", (80,80))
        self.day_bg = create_card("assets/bg/dark_yellow.png", (200, 200), corner_radius=20)
        self.night_icon = create_card("assets/weather/night.png", (75,75))
        self.night_bg = create_card("assets/bg/magenta.png", (200, 200), corner_radius=20)
        
        self.weather_bg_label = tk.Label(self.control_frame)
        self.weather_bg_label.place(x=20, y=153)

        self.weather_icon_label = tk.Label(self.control_frame)
        self.weather_icon_label.place(x=30, y=163)

        self.aqi_bg = create_card("assets/bg/grey.png", (200, 200), corner_radius=20)
        self.aqi_bg_label = tk.Label(self.control_frame, image=self.aqi_bg) # type: ignore
        self.aqi_bg_label.place(x=20, y=375)

        self.clock_bg = create_card("assets/bg/white.png", (140, 40), corner_radius=15)
        self.clock_label = tk.Label(self.control_frame, image=self.clock_bg, bg=AQI_BG_HEX) # type: ignore
        self.clock_label.place(x=30, y=390)
        self.clock_time = tk.Label(self.control_frame, text="00:00 AM", font=('serif', 18), bg="white")
        self.clock_time.place(x=40, y=395)

        WEATHER_LABELS_CONFIG = {'FOR_ALL': {'font': ('serif', 11), 'fg':'white', 'bg':DAY_BG_HEX}}
        self.weather_table = tk.Frame(self.control_frame, bg=DAY_BG_HEX)
        self.weather_table.place(x=30, y=250)
        wp_labels, wv_labels = create_labels(self.weather_table, WEATHER_KEY_PAIR, WEATHER_LABELS_CONFIG)
        self.weather_param_labels, self.weather_val_labels = wp_labels, wv_labels

        AQI_LABELS_CONFIG = {'FOR_ALL': {'font': ('serif', 11), 'fg':'white', 'bg':AQI_BG_HEX}}
        self.aqi_table = tk.Frame(self.control_frame, bg=AQI_BG_HEX)
        self.aqi_table.place(x=30, y=445)
        ap_labels, av_labels = create_labels(self.aqi_table, AQI_KEY_PAIR, AQI_LABELS_CONFIG)
        self.aqi_param_labels, self.aqi_val_labels = ap_labels, av_labels

        self.map_view = MapView(self.map_frame, width=480, height=550, corner_radius=20)
        self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_view.pack(side=tk.RIGHT, padx=20, pady=10)

    def update_data(self) -> None:
        # Get location of input city
        try: loc = self.geoloc.geocode(self.city_entry.get()).raw # type: ignore
        except: messagebox.showinfo("City Not Found","Please enter a valid city name."); return
        
        bbox = loc['boundingbox']
        ptl = (float(bbox[1]), float(bbox[2])) # position top left
        pbr = (float(bbox[0]), float(bbox[3])) # position bottom right

        self.map_view.fit_bounding_box(ptl, pbr)
        self.curr_lat, self.curr_lon = loc['lat'], loc['lon']

        CURRENT_PAYLOAD.update({'q': f"{self.curr_lat},{self.curr_lon}"})
        data = fetch_data(CURRENT_API, CURRENT_PAYLOAD)
        weather_data = data['current'] if data is not None else {} 
        aqi_data = data['current']['air_quality'] if data is not None else {} 
        is_day = data['current']['is_day'] if data is not None else 1 
        timestamp = data['location']['localtime'] if data is not None else "00:00" 
        time = timestamp.split()[1]
        
        if is_day == 0 : 
            self.day_or_night(self.night_icon, self.night_bg, NIGHT_BG_HEX)
            self.clock_time.config(text=(time + " PM"))
        else: 
            self.day_or_night(self.day_icon, self.day_bg, DAY_BG_HEX)
            self.clock_time.config(text=(time + " AM"))

        for label, key in WEATHER_KEY_PAIR.items():
            self.weather_val_labels[label].config(text=f"{weather_data.get(key, 'N/A')}") 
        
        for label, key in AQI_KEY_PAIR.items():
            self.aqi_val_labels[label].config(text=f"{aqi_data.get(key, 'N/A')}") 

    def tplot(self) -> None:
        FORECAST_PAYLOAD.update({'q': f"{self.curr_lat},{self.curr_lon}"})
        data: dict = fetch_data(FORECAST_API, FORECAST_PAYLOAD) # type: ignore
        forecast_day = data['forecast']['forecastday'] if data is not None else {} 

        dates,max_temp,min_temp,avg_temp = [],[],[],[]
        days = range(0, 14)

        for day_data in forecast_day:
            dates.append(day_data['date']) 
            max_temp.append(float(day_data['day']['maxtemp_c'])) 
            min_temp.append(float(day_data['day']['mintemp_c'])) 
            avg_temp.append(float(day_data['day']['avgtemp_c'])) 
        
        temperature_graph(dates, days, max_temp, min_temp, avg_temp)
    def aplot(self) -> None:
        pass
    
    def day_or_night(self, icon, bg_img, bg: str) -> None:
        self.weather_bg_label.config(image=bg_img)

        self.weather_table.config(bg=bg)
        for key, label in self.weather_param_labels.items():
            label.config(bg=bg)
        for key, label in self.weather_val_labels.items():
            label.config(bg=bg)

        self.weather_icon_label.config(image=icon, bg=bg)
        

if __name__ == "__main__":
    app = Current_Weather()
    app.title("Current Weather and Air Quality")
    app.geometry("800x600")
    app.resizable(False, False)
    app.protocol("WM_DELETE_WINDOW", app.quit())
    app.after_idle(app.update_data)
    app.mainloop()
