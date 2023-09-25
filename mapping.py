import folium
from folium.plugins import Fullscreen
import numpy as np


def create_map(cities, map_name="city_map.html"):
    cities = cities + [cities[0]]
    # Extract all the coordinates from the cities
    coordinates = [(np.rad2deg(city.lat), np.rad2deg(city.lng)) for city in cities]
    center_lat = sum(coord[0] for coord in coordinates) / len(coordinates)
    center_lng = sum(coord[1] for coord in coordinates) / len(coordinates)

    # Create a base map
    m = folium.Map(location=[center_lat, center_lng], zoom_start=3)

    # Add markers for each city to the map
    for city in cities:
        folium.Marker(
            location=[np.rad2deg(city.lat), np.rad2deg(city.lng)],
            popup=city.nom,
            icon=folium.Icon(icon="dot", color="black"),
        ).add_to(m)

    folium.PolyLine(locations=coordinates, color='blue').add_to(m)

    m.save(f"maps/{map_name}")  # Save the map to an HTML file

    print("\033[32mSuccessfully created the map\033[0m")
