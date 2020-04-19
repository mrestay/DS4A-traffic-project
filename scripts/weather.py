import datetime
import json
import os
import requests
import pandas as pd
import glob

# replace with '<YOUR-DARKSKY_API-KEY>'
DARKSKY_API_KEY = '4eb053f74d7f5f150083e339c7cb325c'

boroughs_dict = {"usaquen": "4.719722,-74.036667","chapinero": "4.645833,-74.063333","santafe": "4.613889,-74.078611",
"san cristobal": "4.564722,-74.083333","usme": "4.446389,-74.152222","tunjuelito": "4.582222,-74.131944",
"bosa": "4.616944,-74.19","kennedy": "4.643611,-74.153333","fontibon": "4.678611,-74.141111",
"engativa": "4.726111,-74.1","suba": "4.741,-74.084","barrios unidos": "4.678611,-74.078611",
"teusaquillo": "4.670556,-74.093056","los martires": "4.604444,-74.09","antonio nariño": "4.591655,-74.106505",
"puente aranda": "4.6125,-74.106667","la candelaria": "4.591722,-74.074131","rafael uribe": "4.579722,-74.1175",
"ciudadbolivar": "4.536111,-74.138889","sumapaz": "4.26,-74.178333"}


data_folder = '../data/darksky/raw_data'
if not os.path.isdir(data_folder):
    os.makedirs(data_folder)


def date_range(start:datetime.date, end:datetime.date):
    r = (end+datetime.timedelta(days=1)-start).days
    return [str(start+datetime.timedelta(days=i)) + "T00:00:00Z" for i in range(r)]


# Generate the URL
def generate_url(coordinates:str, timestamp:str):
    url = f"https://api.darksky.net/forecast/{DARKSKY_API_KEY}/{coordinates},{timestamp}?units=si&exclude=flags,alerts"
    return url


def fetch_request(url:str):
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


def save_json(weather_json, brough:str):
    current_datetime = datetime.datetime.fromtimestamp(weather_json['currently']['time']).strftime('%Y_%m_%d')
    filename = os.path.join(data_folder, f'weather_{current_datetime}_{brough}.json')
    with open(filename, 'w+') as f:
        f.write(json.dumps(weather_json))


def save_data_to_csv():
    for json_file in glob.glob(data_folder + '/*.json'):
        filename = os.path.basename(json_file).split('.')[0] + '.csv'
        with open(json_file) as f:
            data = json.load(f)
        df = pd.DataFrame(data['hourly']['data'])
        # Convert time into a proper datetime object
        df['time'] = pd.to_datetime(df['time'], unit='s')
        #save file
        output_folder_name = '../data/darksky/output_data'
        if not os.path.isdir(output_folder_name):
            os.makedirs(output_folder_name)
        filename = os.path.join(output_folder_name, filename)
        df.to_csv(filename, index=False)

if __name__ == "__main__":
    start = datetime.date(2020,4,13)
    end = datetime.date(2020,4,17)
    date_list = date_range(start, end)

    borough = 'usaquen'
    coords = boroughs_dict[borough]
    date =date_list[3]
    print(f'fetch weather data for {borough} with coordinates {coords} for day {date}')
    test_url = generate_url(coords,date)
    save_json(fetch_request(test_url), borough)
    save_data_to_csv()