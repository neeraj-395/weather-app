import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


def temp_graph(dates: List[str], days: range, max_temp: List[float], min_temp: List[float], avg_temp: Optional[List[float]] = None) -> None:
    """
    Generates a temperature graph displaying daily temperature variations.

    This function creates a filled contour plot showing the variation of temperatures 
    over a range of days. It plots the minimum, maximum, and optionally the average 
    temperatures for each day.

    ## Args:
        dates (List[str]): A list of date strings corresponding to the days.
        days (range): A range object representing the days.
        max_temp (List[float]): A list of maximum temperatures for each day.
        min_temp (List[float]): A list of minimum temperatures for each day.
        avg_temp (Optional[List[float]]): An optional list of average temperatures for each day.

    ## Example:
        >>> dates = ["2023-05-01", "2023-05-02", "2023-05-03"]
        >>> days = range(1, 4)
        >>> max_temp = [25.0, 27.0, 22.0]
        >>> min_temp = [15.0, 17.0, 12.0]
        >>> temperature_graph(dates, days, max_temp, min_temp)

    ## Note:    
    This function documentation was generated with the assistance of ChatGPT, 
    an AI language model developed by OpenAI.
    """

    ''' Maximum Temperature in Celsius '''
    MIN_TEMP_C = 0
    ''' Minimum Temperature in Celcius '''
    MAX_TEMP_C = 55

    if avg_temp is None:
       avg_temp = [(max_temp[i] + min_temp[i]) / 2 for i in range(len(max_temp))]
    
    plt.figure(figsize=(10, 6))

    norm = Normalize(MIN_TEMP_C, MAX_TEMP_C)

    X, Y = np.meshgrid(days, np.linspace(MIN_TEMP_C, MAX_TEMP_C, 100))

    plt.contourf(X, Y, Y, 500, cmap=plt.cm.jet) # type: ignore

    plt.fill_between(days, MIN_TEMP_C, min_temp, color='white')
    plt.fill_between(days, max_temp, MAX_TEMP_C, color='white')
    
    plt.plot(days, avg_temp, color='white', marker='o', markerfacecolor="red",linewidth=2, label='Average Temperature')
    plt.colorbar(ScalarMappable(cmap=plt.cm.jet, norm=norm), ax=plt.gca(), label='Temperature (°C)') # type: ignore

    plt.xticks(days, dates, rotation=45, ha='right')

    plt.ylabel('Temperature (°C)')
    plt.title('Daily Temperature Variation')

    plt.xticks(days)
    plt.legend()
    plt.tight_layout()
    plt.show()


def aqi_graph(pm2_5: List[float], pm10: List[float], so2: List[float]):
    """
    Generate a plot showing the concentration levels of PM2.5, PM10, and SO2 pollutants over time,
    along with the World Health Organization (WHO) recommended limits for each pollutant.

    ## Parameters:
    - pm2_5 (List[float]): A list of PM2.5 concentration levels measured over time.
    - pm10 (List[float]): A list of PM10 concentration levels measured over time.
    - so2 (List[float]): A list of SO2 concentration levels measured over time.

    ## Example:
        >>> pm2_5 = [20, 25, 30, 40, 35]
        >>> pm10 = [30, 35, 45, 50, 55]
        >>> so2 = [15, 18, 22, 19, 21]
        >>> aqi_graph(pm2_5, pm10, so2)
    
    ## Note:    
    This function documentation was generated with the assistance of ChatGPT, 
    an AI language model developed by OpenAI.
    """

    # WHO Recommended limits for other pollutants
    WHO_LIMITS = {'PM2.5': 35, 'PM10': 50, 'SO2': 20}
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plotting PM2.5 AQI as scatter plot
    plt.plot(np.arange(len(pm2_5)), pm2_5, label='PM2.5', color='blue')
    plt.axhline(y=WHO_LIMITS['PM2.5'], color='green', linestyle='-', label='WHO Recommended Limit (PM2.5)')
    
    # Plotting PM10 AQI as scatter plot
    plt.plot(np.arange(len(pm10)), pm10, label='PM10', color='red')
    plt.axhline(y=WHO_LIMITS['PM10'], color='orange', linestyle='-', label='WHO Recommended Limit (PM10)')

    # Plotting PM10 AQI as scatter plot
    plt.plot(np.arange(len(so2)), so2, label='PM10', color='purple')
    plt.axhline(y=WHO_LIMITS['SO2'], color='black', linestyle='-', label='WHO Recommended Limit (SO2)')

    # Formatting the plot
    plt.title('PM2.5, PM10 And SO Concentration Levels')
    plt.ylabel('Concentration (µg/m³ or ppm)')
    plt.xlabel('Month Ago')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


