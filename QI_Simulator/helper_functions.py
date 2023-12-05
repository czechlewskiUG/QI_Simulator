import json
import math


from geopy.distance import geodesic as GD
from geopy.geocoders import Bing


PATH_NODES = "../data/nodes.json"
PATH_EDGES = "../data/edges.json"


def calculate_length(edges_data):

    with open(PATH_NODES, "r", encoding="utf-8") as read_file:
        nodes_data = json.load(read_file)
    
    for edge in edges_data:
        node_1 = next(node for node in nodes_data if node["id"] == edge["connection"]["node_id_1"])
        node_2 = next(node for node in nodes_data if node["id"] == edge["connection"]["node_id_2"])
        node_1_coor = (node_1["coordinates"]["latitude"], node_1["coordinates"]["longitude"])
        node_2_coor = (node_2["coordinates"]["latitude"], node_2["coordinates"]["longitude"])
        edge["length"] = math.ceil(GD(node_1_coor, node_2_coor).km)

    return edges_data

def add_id(json_data):

    for i, node in enumerate(json_data):
        node["id"] = i + 1

    return json_data

def sort_by_city(nodes_data):
     
     return sorted(nodes_data, key=lambda d: d['city']) 

def get_coordinates(nodes_data):

    # One has to put here a valid Bing api_key
    geolocator = Bing(api_key="qwerty")

    for node in nodes_data:
        if "Węzeł sieci Pionier" not in node["type"]:
            location = geolocator.geocode(node["address"])
            print((location.latitude, location.longitude))
            node["coordinates"]["latitude"] = location.latitude
            node["coordinates"]["longitude"] = location.longitude

    return nodes_data

def change_json_file(path):

    with open(path, "r", encoding="utf-8") as read_file:
        json_data = json.load(read_file)

    calculate_length(json_data)
    # json_data = add_id(json_data)
    # json_data = sort_by_city(json_data)
    # json_data = get_coordinates(json_data)

    with open(path, "w", encoding="utf-8") as write_file:
        json.dump(json_data, write_file, ensure_ascii=False)

def main():

    change_json_file(PATH_EDGES)
    

if __name__ == "__main__":
    main()
