import folium
from folium.plugins import MarkerCluster
import json

# define coordinates for boundary box
min_lat, max_lat = 25.0, 32.0
min_lon, max_lon = -90.0, -75.0

# Read the location data from the JSON file
with open('../static/json/weather_stations.json') as f:
    locations = json.load(f)

# Create map centered on Florida
florida_map = folium.Map(
    location=[28.0, -82.5],
    tiles="CartoDB dark_matter",
    zoom_start = 7,
    min_zoom = 7,
    zoom_control= False,
)

# Create a legend for the colors
legend_html = """
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 400px; height: 200px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color: rgba(255, 255, 255, 0.7);
     ">&nbsp; Trend Precip Yearly <br>
     &nbsp; -2 or less &nbsp; <i class="fa fa-map-marker fa-2x" style="color:red"></i><br>
     &nbsp; -2 to 0 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:orange"></i><br>
     &nbsp; 0 to 2 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:green"></i><br>
     &nbsp; 2 or more &nbsp; <i class="fa fa-map-marker fa-2x" style="color:lightgreen"></i>
</div>
"""
florida_map.get_root().html.add_child(folium.Element(legend_html))

# Add markers for each location
for location in locations:
    # Get the trend_meantemp_yearly value for the current location
    trend = location['trend_precip_yearly']
    
    # Set the color of the marker based on the trend value
    if trend < -2:
        color = 'red'
    elif trend >= -2 and trend <= 0:
        color = 'orange'
    elif trend >= 0 and trend <= 2:
        color = 'lightgreen'
    elif trend > 2:
        color = 'green'
        
    popup_html = "<b>{station_name} ({station_id})</b><br>lat: {station_lat}, lon: {station_lon}<br><a href='../../static/img/plots/trends/precip_yearly/{station_id}_precip_trend_yearly.png' target='_BLANK'><img src='../../static/img/plots/trends/precip_yearly/{station_id}_precip_trend_yearly.png' width='100%' height='100%'></a>".format(
        station_name=location['station_name'],
        station_id=location['station_id'],
        station_lat=location['station_lat'],
        station_lon=location['station_lon']
    )

    marker = folium.Marker(
        location=(location["station_lat"],location["station_lon"]), 
        icon=folium.Icon(color=color),
        popup=folium.Popup(html=popup_html, max_width=1000, min_width=500)
    )
    marker.add_to(florida_map)

# Save map as HTML file
florida_map.save('../template/maps/map_trend_precip_yearly.html')