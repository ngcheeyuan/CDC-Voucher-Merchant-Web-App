# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from dash import dcc , html
from dash.dependencies import Input, Output

#----------------------------------------------------------------------------------------------------------------
df = pd.read_csv('labelled_df.csv')
mrt_list = df['nearest_station'].dropna().unique().tolist()
mrt_options = [{'label':x,'value':x} for x in sorted(mrt_list)]

#----------------------------------------------------------------------------------------------------------------
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(children=[
        html.Label('Merchant Type'),
        dcc.Dropdown(
          id='merchant_selected',
          style = {"width":"40%"},
          options=[{'label': 'All', 'value': 'All'},
          {'label': 'Bakery', 'value': 'Bakery'},
          {'label': 'Beauty', 'value': 'Beauty'},
          {'label': 'Dry food', 'value': 'Dry food'},
          {'label': 'Florist', 'value': 'Florist'},
          {'label': 'Food', 'value': 'Food'},
          {'label': 'Health', 'value': 'Health'},
          {'label': 'Minimart', 'value': 'Minimart'},
          {'label': 'Mobile services', 'value': 'Mobile services'},
          {'label': 'Others', 'value': 'Others'},
          {'label': 'Tailor/fashion', 'value': 'Tailor/fashion'},
          {'label': 'unllabelled', 'value': 'unllabelled'}],
            value='Food'
        ),

        html.Br(),
        html.Label('Select Nearest Mrt'),
        dcc.Dropdown(
            id='nearest_mrt_selected',
            style = {"width":"40%"},
            options=mrt_options,
            value='ADMIRALTY',
            multi=False
        ),
        html.Br(),
        html.Div(id ='output_container'),
        html.Br(),
        html.Iframe(id='map', srcDoc=None, width='1200', height='600', hidden=False),
    ], style={'padding': 10, 'flex': 1}),
], style={'display': 'flex', 'flex-direction': 'row'})

#----------------------------------------------------------------------------------------------------------------
@app.callback(
     [Output(component_id = 'output_container', component_property = 'children'),
     Output(component_id = 'map', component_property = 'srcDoc')],
     [Input(component_id = 'nearest_mrt_selected', component_property = 'value'),
     Input(component_id = 'merchant_selected', component_property = 'value')])
#----------------------------------------------------------------------------------------------------------------
def update_figure(nearest_mrt_selected,merchant_selected):
    print(nearest_mrt_selected,merchant_selected)
    if merchant_selected == 'All':
        mask = df['nearest_station'] == nearest_mrt_selected
        temp_df = df[mask].copy()

        if len(temp_df) == 0:
            lat = 1.34919
            lon = 103.82

            container = "There are no merchants found, please try something else"

        else:
            lat = temp_df['latitude'].mean()
            lon = temp_df['longitude'].mean()

            container = "Loading the map!"

        m=folium.Map(location=[lat,lon],
                     zoom_start=13,
                     min_zoom=12,
                     max_zoom=19)
        marker_cluster = MarkerCluster().add_to(m)


        for index,row in temp_df.iterrows():
            folium.Marker(location=[row['latitude'], row['longitude']],
                          popup=row['name'],
                         ).add_to(marker_cluster)

        m.save("mymapnew.html")

        return container,open('mymapnew.html', 'r').read()
    else:

        mask = df['nearest_station'] == nearest_mrt_selected
        mask1 = df['label'] == merchant_selected
        temp_df = df[mask&mask1].copy()

        if len(temp_df) == 0:
            lat = 1.34919
            lon = 103.82

            container = "There are no merchants found, please try something else"
        else:
            lat = temp_df['latitude'].mean()
            lon = temp_df['longitude'].mean()

            container = "Loading the map!"

        m=folium.Map(location=[lat,lon],
                     zoom_start=13,
                     min_zoom=12,
                     max_zoom=19)
        marker_cluster = MarkerCluster().add_to(m)


        for index,row in temp_df.iterrows():
            folium.Marker(location=[row['latitude'], row['longitude']],
                          popup=row['name'],
                         ).add_to(marker_cluster)

        m.save("mymapnew.html")

        return container, open('mymapnew.html', 'r').read()



if __name__ == '__main__':
    app.run_server(debug=True)