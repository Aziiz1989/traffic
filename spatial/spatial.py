import numpy as np
import matplotlib.pylab as plt
from h3 import h3
import folium
import math
import pandas as pd

def df_to_geojson(df, id_='null', points='pnts',properties=''):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'id':row[id_],
                   'properties':{},
                   'geometry':{'type':'Polygon',
                               'coordinates':[]}}
        reversedOder=[[i[1],i[0]] for i in row[points]]
        feature['geometry']['coordinates'] = [reversedOder]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)

    return geojson

def geo_hashing(row, resolution):
    if pd.isna(row["lat"]) | pd.isna(row["long"]) :
        return -1;
    else:
         hexa=h3.geo_to_h3(row["lat"],row["long"],resolution)
         return hexa+[hexa[0]]


#this function needs the the dataframe to have lat and lon
def generate_hex_heatmap(data,
                         aggregateThis="count",
                         outpath="index.html",
                         h3_resolution=8,
                         map_zoom_level=11,
                         midpoint=[24.71284, 46.70490],
                         outputPath="",
                         logScale=False):


    data["h3_cell"]=data.apply(lambda row: h3.geo_to_h3(row["lat"],row["long"],h3_resolution) ,axis=1)
    data['hexagonPoints']=data.apply(lambda x: h3.h3_to_geo_boundary(x["h3_cell"]),axis=1)

    #do the aggregation of data
    if aggregateThis=="count":
        data["count"]=1
    cells_count=data.groupby("h3_cell").sum()[aggregateThis]
    AggCount=pd.DataFrame(cells_count)
    AggCount=AggCount.reset_index()
    if logScale:
        log_aggregateThis='{}{}{}'.format('log(',aggregateThis,')')
        AggCount[log_aggregateThis]=AggCount.apply(lambda x:  math.log(x[aggregateThis],10),axis=1)

    AggCount['hexagonPoints']=AggCount.apply(lambda x: h3.h3_to_geo_boundary(x["h3_cell"]),axis=1)

    #get the geoJson
    geoJson=df_to_geojson(AggCount,id_="h3_cell",points="hexagonPoints")

    AggCount=AggCount[AggCount['h3_cell']!='0']

    m = folium.Map(midpoint,tiles='stamentoner', zoom_start=map_zoom_level)

    if logScale:
        param=log_aggregateThis;
    else:
        param=aggregateThis;
    m.choropleth(
     geo_data=geoJson,
     name='choropleth',
     data=AggCount,
     columns=['h3_cell',param],
     key_on='feature.id',
     fill_color='YlOrRd',
     fill_opacity=0.7,
     line_opacity=0.2,
     legend_name=param
    )
    folium.LayerControl().add_to(m)

    m.save(outpath)


