import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

''' Maximum Temperature in Celsius '''
MIN_TEMP_C = 0
''' Minimum Temperature in Celcius '''
MAX_TEMP_C = 56

def temperature_graph(dates: List[str], days: range, max_temp: List[float], min_temp: List[float], avg_temp: Optional[List[float]] = None) -> None:
    """
    Generates a temperature graph displaying daily temperature variations.

    This function creates a filled contour plot showing the variation of temperatures 
    over a range of days. It plots the minimum, maximum, and optionally the average 
    temperatures for each day.

    Args:
        dates (List[str]): A list of date strings corresponding to the days.
        days (range): A range object representing the days.
        max_temp (List[float]): A list of maximum temperatures for each day.
        min_temp (List[float]): A list of minimum temperatures for each day.
        avg_temp (Optional[List[float]]): An optional list of average temperatures for each day.

    Example:
        >>> dates = ["2023-05-01", "2023-05-02", "2023-05-03"]
        >>> days = range(1, 4)
        >>> max_temp = [25.0, 27.0, 22.0]
        >>> min_temp = [15.0, 17.0, 12.0]
        >>> temperature_graph(dates, days, max_temp, min_temp)

    Note:    
    This function documentation was generated with the assistance of ChatGPT, 
    an AI language model developed by OpenAI.
    """

    if avg_temp is None:
       avg_temp = [(max_temp[i] + min_temp[i]) / 2 for i in range(len(max_temp))]

    norm = Normalize(min(min_temp), max(max_temp))

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

def aqi_graphs():
    pass
