import pandas as pd
import geopandas
import sqlalchemy
# RDS connection
connection_uri = 'postgres+psycopg2://postgres:nOocvi5MWwXqoyITp5Z7m2Je5JXBlDlznqCFCsLX@ds4a.czdm3x741xmp.us-east-1.rds.amazonaws.com/ds4a'
engine = sqlalchemy.create_engine(connection_uri)
# Read main dataset
accidents = pd.read_sql_table("accidents", con=engine)

# accidents_All1 = accidents_All[accidents_All['sample_type'] == 1]

# temperature
agg = ['mean', 'min', 'median', 'max']
t_year = accidents[['year', 'temperature']].groupby('year').agg(agg)

temperature = t_year.temperature.transpose()

# precipitation
p_year = accidents[['year', 'precipIntensity']].groupby('year').agg(agg)

precipitation = p_year.precipIntensity.transpose()


# bourought

# borough_file = os.path.join(data_folder, 'poligonos-localidades.geojson')
# borough_df = geopandas.read_file(borough_file, driver= "GeoJSON")
# borough_df.drop(columns = ['Acto administrativo de la localidad', 'Area de la localidad'], inplace=True)
# borough_df.rename(columns={'Nombre de la localidad':'borough', 'Area de la localidad':'area',
#                            'Identificador unico de la localidad':'id' }, inplace=True)
# borough_df.id = borough_df.id.astype(int)
#
# borough_info = os.path.join(data_folder, 'localidades.csv')
# borough_info = pd.read_csv(borough_info, header=0, dtype='str')
# borough_info.area_km2 = borough_info.area_km2.astype('float')
# borough_info.population = borough_info.population.astype('int')
# borough_info.population_density = borough_info.population_density.astype('float')
# borough_info.id = borough_info.id.astype(int)
#
# borough_df = borough_df.merge(borough_info, how='inner', left_on='id', right_on='id')
# borough_df.drop(columns = ['borough_y'], inplace=True)
# borough_df.rename(columns={'borough_x':'borough'}, inplace=True)
#
# # set(accidents.borough.unique()) - set(borough_df['borough'].unique())
# # st.write(accidents)
#
# by_borough = accidents[['borough_geo','accident_id']].groupby(['borough_geo']).count().reset_index().sort_values(by='accident_id',ascending=False)
# by_borough = by_borough.reset_index(drop=True)
# by_borough.rename(columns={'accident_id':'accident_count'}, inplace=True)
# #
# borough_data = borough_df.merge(by_borough, how='left', left_on='borough', right_on='borough_geo')
# #
# borough_data['accident_density'] = round(borough_data.accident_count/borough_data.area_km2, 1)
# borough_data['accident_density_population'] = borough_data.accident_count/borough_data.population
#
#
# aa = borough_data
#
# with open('data1.json', 'w') as f:
#   f.write(borough_data.to_json())
#
# # Custom color scale
# COLOR_RANGE = [
#     [65, 182, 196],
#     [127, 205, 187],
#     [199, 233, 180],
#     [237, 248, 177],
#     [255, 255, 204],
#     [255, 237, 160],
#     [254, 217, 118],
#     [254, 178, 76],
#     [253, 141, 60],
#     [252, 78, 42],
#     [227, 26, 28],
#     [189, 0, 38],
#     [128, 0, 38],
# ]
#
# BREAKS = [-0.6, -0.45, -0.3, -0.15, 0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2]
#
#
# def color_scale(val):
#     for i, b in enumerate(BREAKS):
#         if val < b:
#             return COLOR_RANGE[i]
#     return COLOR_RANGE[i]
#
#
# json = pd.read_json('data1.json')
# df = pd.DataFrame()
# df["coordinates"] = json["features"].apply(lambda row: row["geometry"]["coordinates"])
# df["accident_density"] = json["features"].apply(lambda row: row["properties"]["accident_density"])
# df["accident_count"] = json["features"].apply(lambda row: row["properties"]["accident_count"])
# df["fill_color"] = json["features"].apply(lambda row: color_scale(row["properties"]["accident_count"]))
#
#
# borough_data = df

#Clusters
centroids = pd.read_sql_table('centroids', con=engine)

clustered_points = pd.read_sql_table('clusters', con=engine)
