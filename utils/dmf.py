import requests
from tkinter import messagebox
from typing import Optional, Dict, Tuple

def fetch_data(api_url: str, payload: Optional[Dict[str,str]] = None) -> Dict:
    """
    Fetches data from the specified API URL with optional query parameters.

    This function sends a GET request to the provided API URL, optionally with
    query parameters. It checks if the response content type is JSON and returns
    the parsed JSON data. If the content type is not JSON, it returns None. In case
    of a request exception, an error message is displayed and None is returned.

    ### Example:
        >>> api_url = "https://api.example.com/data"
        >>> params = {"param1": "value1", "param2": "value2"}
        >>> data = fetch_data(api_url, params)
        >>> if data:
        >>>     print("Data fetched successfully:", data)
        >>> else:
        >>>     print("Failed to fetch data or data is not in JSON format.")

    ### Note:
    This function documentation was generated with the assistance of ChatGPT, 
    an AI language model developed by OpenAI.
    """
    try:
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        type = response.headers.get('Content-Type')

        if type and "application/json" in type:
            return response.json()
        else: return {}
    
    except requests.exceptions.HTTPError as e:
        title, message = throw_error(e)
        messagebox.showerror(title, message)
        return {}

    
def throw_error(e: requests.exceptions.HTTPError) -> Tuple[str,str]:
    """
    Maps HTTP error codes to user-friendly error messages.

    ### Parameters:
    e (requests.exceptions.HTTPError): The HTTP error exception object.

    ### Returns:
    Tuple[str, str]: A tuple containing the error title and detailed error message.

    ### Note:
    This function documentation was generated with the assistance of ChatGPT, 
    an AI language model developed by OpenAI.
    """

    if e.response.status_code == 400:
        return ('Bad Request', 'The request was invalid.')
    elif e.response.status_code == 401:
        return ('Unauthorized','API key is invalid or missing.')
    elif e.response.status_code == 403:
        return ('Forbidden','Access is not allowed.')
    elif e.response.status_code == 404:
        return ('Not Found','The requested resource could not be found.')
    elif e.response.status_code == 429:
        return ('Too Many Requests','Rate limit exceeded.')
    elif e.response.status_code == 500:
        return ('Internal Server Error','An error occurred on the server.')
    else:
        return ('HTTP error occurred',f"{e}")