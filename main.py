import tkinter as tk
from datetime import timezone
from tkinter import messagebox
from utils.dmf import fetch_data
from datetime import datetime as dt
from geopy.geocoders import Nominatim
from utils.plots import temp_graph, aqi_graph
from utils.gui import create_card, create_labels
from dateutil.relativedelta import relativedelta
from tkintermapview import TkinterMapView as MapView

''' API CREDENTIALS '''
CURRENT_WEATHER_API = "https://api.weatherapi.com/v1/current.json"
WEATHER_FORECAST_API = "https://api.weatherapi.com/v1/forecast.json"
AQI_HISTORY_API = "http://api.openweathermap.org/data/2.5/air_pollution/history"
MAP_TILE_API = "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga"

WEATHER_API_KEY = "a78578373e714abbabf51022241205"
OPEN_WEATHER_API_KEY = "b0011235ef5bece1b52b26b323021eb9"

''' API DATA KEY PAIRS'''
WEATHER_KEY_PAIR = {
    'Temp (°C)': 'temp_c', 
    'Humidity (%)': 'humidity', 
    'Wind (m/s)':'wind_kph', 
    'Pressure (hPa)': 'pressure_mb'
}
AQI_KEY_PAIR = {
    'PM2.5 (μg/m3)':'pm2_5','PM10 (μg/m3)':'pm10',
    'Ozone (μg/m3)':'o3','CO (μg/m3)':'co',
    'Sulphur (μg/m3)':'so2'
}

''' HEX CODE OF CARDS BACKGROUND'''
DAY_BG_HEX = "#F29F05"
NIGHT_BG_HEX = "#890189"
AQI_BG_HEX = "#616161"

class Current_Weather(tk.Tk):
    def __init__(self):
        ''' Initialize the Current_Weather class. '''
        super().__init__()

        self.geoloc = Nominatim(user_agent="Weather_App")
    
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.map_frame = tk.Frame(self.main_frame)
        self.map_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.city_label = tk.Label(self.control_frame)
        self.city_label.config(text="Enter City/State:", font=('serif',12), justify='center')
        self.city_label.pack(side=tk.TOP, pady=(15,5), anchor='center', padx=(20,5))

        self.search_frame = tk.Frame(self.control_frame)
        self.search_frame.pack(side=tk.TOP, fill=tk.X, padx=(20,5))

        self.city_entry = tk.Entry(self.search_frame, fg='white', justify='center', font=('', 11))
        self.city_entry.config(highlightthickness=0, insertbackground='white', bg='black')
        self.city_entry.insert(0, "India")
        self.city_entry.grid(row=0, column=0, ipady=6, sticky='w')

        self.search_icon = create_card("assets/other/search.png", (30, 30))
        search_button = tk.Button(self.search_frame, image=self.search_icon) # type: ignore
        search_button.config(cursor='hand2', fg='black', bg='black', command=self.update_data)
        search_button.grid(row=0, column=1, sticky='w')
        
        self.btn_frame = tk.Frame(self.control_frame)
        self.btn_frame.pack(side=tk.TOP, pady=10, padx=(20,5), anchor='center')

        tplot_btn = tk.Button(self.btn_frame, command=self.tplot)
        tplot_btn.config(text="T-Plot", bg="black", fg="white", font=('',11))
        tplot_btn.pack(side=tk.LEFT, padx=10)

        aplot_btn = tk.Button(self.btn_frame, command=self.aplot)
        aplot_btn.config(text="A-Plot", bg="black", fg="white", font=('',11))
        aplot_btn.pack(side=tk.RIGHT, padx=10)

        self.card_frame = tk.Frame(self.control_frame)
        self.card_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=(20,5), pady=(5, 10), anchor='n')

        self.night_bg = create_card("assets/bg/magenta.png", (200, 200), corner_radius=20)
        self.day_bg = create_card("assets/bg/dark_yellow.png", (200, 200), corner_radius=20)
        self.weather_bg_label = tk.Label(self.card_frame)
        self.weather_bg_label.grid(row=0, padx=10, pady=10)

        self.aqi_bg = create_card("assets/bg/grey.png", (200, 200), corner_radius=20)
        self.aqi_bg_label = tk.Label(self.card_frame, image=self.aqi_bg) # type: ignore
        self.aqi_bg_label.grid(row=1, padx=10, pady=10)

        self.day_icon = create_card("assets/weather/day.png", size=(80,80))
        self.night_icon = create_card("assets/weather/night.png", size=(75,75))
        self.weather_icon_label = tk.Label(self.weather_bg_label)
        self.weather_icon_label.place(x=10, y=10)

        self.clock_bg = create_card("assets/bg/white.png", (140, 40), corner_radius=15)
        self.clock_label = tk.Label(self.aqi_bg_label, image=self.clock_bg, bg=AQI_BG_HEX) # type: ignore
        self.clock_label.place(x=10, y=5)
        self.clock_time = tk.Label(self.clock_label, font=('serif', 18), bg="white")
        self.clock_time.pack(padx=10, pady=10)

        WEATHER_LABELS_CONFIG = {'FOR_ALL': {'font': ('serif', 11), 'fg':'white', 'bg':DAY_BG_HEX}}
        self.weather_table = tk.Frame(self.weather_bg_label, bg=DAY_BG_HEX)
        self.weather_table.place(x=10, y=95)
        wp_labels, wv_labels = create_labels(self.weather_table, WEATHER_KEY_PAIR, WEATHER_LABELS_CONFIG)
        self.weather_param_labels, self.weather_val_labels = wp_labels, wv_labels

        AQI_LABELS_CONFIG = {'FOR_ALL': {'font': ('serif', 11), 'fg':'white', 'bg':AQI_BG_HEX}}
        self.aqi_table = tk.Frame(self.aqi_bg_label, bg=AQI_BG_HEX)
        self.aqi_table.place(x=10, y=70)
        ap_labels, av_labels = create_labels(self.aqi_table, AQI_KEY_PAIR, AQI_LABELS_CONFIG)
        self.aqi_param_labels, self.aqi_val_labels = ap_labels, av_labels

        self.map_view = MapView(self.map_frame, width=550, height=550, corner_radius=20)
        self.map_view.set_tile_server(MAP_TILE_API, max_zoom=22)
        self.map_view.pack(side=tk.TOP, padx=20, pady=20, anchor='e')

    def update_data(self) -> None:
        try: loc = self.geoloc.geocode(self.city_entry.get())
        except: messagebox.showinfo("City Not Found","Please enter a valid city name."); return
        
        bbox = loc.raw['boundingbox'] # type: ignore
        ptl = (float(bbox[1]), float(bbox[2])) # position top left
        pbr = (float(bbox[0]), float(bbox[3])) # position bottom right

        self.map_view.fit_bounding_box(ptl, pbr)
        self.curr_lat, self.curr_lon = loc.raw['lat'], loc.raw['lon'] # type: ignore

        PAYLOAD = {
            'q': f"{self.curr_lat},{self.curr_lon}", 
            'key': WEATHER_API_KEY, 
            'aqi':'yes'
        }

        data = fetch_data(CURRENT_WEATHER_API, PAYLOAD)
        weather_data = data.get('current', {})
        aqi_data = data.get('current', {}).get('air_quality', {})
        is_day = data.get('current', {}).get('is_day', 1)
        timestamp = data.get('location', {}).get('localtime', '2004-01-19 00:00')
        time = dt.strptime(timestamp, '%Y-%m-%d %H:%M').strftime('%H:%M')
        
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

        PAYLOAD = {
            'q': f"{self.curr_lat},{self.curr_lon}",
            'key': WEATHER_API_KEY,
            'days':'14',
            'hours':'-1'
        }

        data: dict = fetch_data(WEATHER_FORECAST_API, PAYLOAD)
        if not data: return

        forecast_day = data['forecast']['forecastday']

        dates,max_temp,min_temp,avg_temp = [],[],[],[]
        days = range(0, 14)

        for day_data in forecast_day:
            dates.append(day_data['date']) 
            max_temp.append(float(day_data['day']['maxtemp_c'])) 
            min_temp.append(float(day_data['day']['mintemp_c'])) 
            avg_temp.append(float(day_data['day']['avgtemp_c'])) 
        
        temp_graph(dates, days, max_temp, min_temp, avg_temp)
    
    def aplot(self) -> None:
       # Gee current date and time
        current_date = dt.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Subtract one month from the current date
        one_month_back_date = current_date - relativedelta(months=1)

        # Convert both dates to UNIX timestamps
        start_unix = int(one_month_back_date.replace(tzinfo=timezone.utc).timestamp())
        end_unix = int(current_date.replace(tzinfo=timezone.utc).timestamp())
        
        PAYLOAD = {
            'lat': self.curr_lat,
            'lon': self.curr_lon,
            'start': start_unix,
            'end': end_unix,
            'appid': OPEN_WEATHER_API_KEY
        }

        data: dict = fetch_data(AQI_HISTORY_API, PAYLOAD)
        if not data: return

        pm2_5, pm10, so2 = [], [], []

        for entry in data['list']:
            pm2_5.append(entry['components']['pm2_5'])
            pm10.append(entry['components']['pm10'])
            so2.append(entry['components']['so2'])

        aqi_graph(pm2_5, pm10, so2)

    
    def day_or_night(self, icon, bg_img, bg: str) -> None:
        self.weather_bg_label.config(image=bg_img)

        self.weather_table.config(bg=bg)
        for label in self.weather_param_labels.values():
            label.config(bg=bg)
        for label in self.weather_val_labels.values():
            label.config(bg=bg)

        self.weather_icon_label.config(image=icon, bg=bg)
        

if __name__ == "__main__":
    app = Current_Weather()
    app.title("Weather and Air Quality Analyzer")
    app.geometry("800x600")
    app.resizable(False, False)
    app.protocol("WM_DELETE_WINDOW", app.quit())
    app.after_idle(app.update_data)
    app.mainloop()