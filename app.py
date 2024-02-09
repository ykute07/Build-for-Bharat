import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt

class OpenStreetMapSDK:
    def __init__(self):
        self.graph = None

    def create_graph_from_polygon(self, polygon):
        self.graph = ox.graph_from_polygon(polygon, network_type='drive')

    def generate_motorable_path(self, source_point, target_point):
        if not self.graph:
            raise ValueError("Graph not initialized. Please create a graph first.")

        source_node = ox.get_nearest_node(self.graph, source_point)
        target_node = ox.get_nearest_node(self.graph, target_point)
        path = nx.shortest_path(self.graph, source_node, target_node)

        return path

    def reverse_geocode(self, address):
        location = ox.geocode(address)
        point = Point(location['lon'], location['lat'])
        
        return point

    def compute_motorable_distance(self, source_point, target_point):
        if not self.graph:
            raise ValueError("Graph not initialized. Please create a graph first.")

        source_node = ox.get_nearest_node(self.graph, source_point)
        target_node = ox.get_nearest_node(self.graph, target_point)
        distance = nx.shortest_path_length(self.graph, source_node, target_node, weight='length')

        return distance

    def plot_graph(self):
        if not self.graph:
            raise ValueError("Graph not initialized. Please create a graph first.")

        fig, ax = ox.plot_graph(self.graph, node_color='b', node_size=30, node_alpha=0.5, edge_color='r')

if __name__ == "__main__":
    sdk = OpenStreetMapSDK()

    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])

    sdk.create_graph_from_polygon(polygon)

    source_point = (0.1, 0.1)
    target_point = (0.9, 0.9)
    path = sdk.generate_motorable_path(source_point, target_point)
    print("Motorable Path:", path)

    address = "New York City, USA"
    point = sdk.reverse_geocode(address)
    print("Reverse Geocoded Point:", point)

    distance = sdk.compute_motorable_distance(source_point, target_point)
    print("Motorable Distance:", distance)

    sdk.plot_graph()
    plt.show()
