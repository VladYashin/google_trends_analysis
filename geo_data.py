import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import numpy as np

shapefile = 'gpd_shapefiles/vg2500_bld.shp'
# shapefile = 'gpd_shapefiles/2_hoch.geo.json'

excl = pd.read_excel('google_trends_kw.xlsx', sheet_name='Datenbasis (By region)')
df_ibr = pd.DataFrame(excl)

map_df = gpd.read_file(shapefile)

merged_dfs = map_df.set_index('GEN').join(df_ibr.set_index('geoName'))

