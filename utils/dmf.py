import requests
from tkinter import messagebox
from typing import Optional, Dict

def fetch_data(api_url: str, payload: Optional[Dict[str,str]] = None) -> Dict | None:
    """
    Fetches data from the specified API URL with optional query parameters.

    This function sends a GET request to the provided API URL, optionally with
    query parameters. It checks if the response content type is JSON and returns
    the parsed JSON data. If the content type is not JSON, it returns None. In case
    of a request exception, an error message is displayed and None is returned.

    ## Example:
        >>> api_url = "https://api.example.com/data"
        >>> params = {"param1": "value1", "param2": "value2"}
        >>> data = fetch_data(api_url, params)
        >>> if data:
        >>>     print("Data fetched successfully:", data)
        >>> else:
        >>>     print("Failed to fetch data or data is not in JSON format.")

    ## Note:
    This function documentation was generated with the assistance of ChatGPT, 
    an AI language model developed by OpenAI.
    """
    try:
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        type = response.headers.get('Content-Type')

        if type and "application/json" in type:
            return response.json()
        else: return None
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return None