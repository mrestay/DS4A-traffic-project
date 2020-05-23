import requests
import pandas as pd

DARKSKY_API_KEY = '4eb053f74d7f5f150083e339c7cb325c'


# Generate the URL
def generate_url(coordinates: str):
    url = f"https://api.darksky.net/forecast/{DARKSKY_API_KEY}/{coordinates}?units=si&exclude=flags,alerts"
    return url


# fecth the request
def fetch_request(url: str):
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


def get_dataframe(x_coord: float, y_coord: float):
    coords = f'{x_coord},{y_coord}'
    url_request = generate_url(coords)
    data = fetch_request(url_request)
    df = pd.DataFrame(data['hourly']['data'])
    # Convert time into a proper datetime object
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
