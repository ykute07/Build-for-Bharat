import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt

class OpenStreetMapSDK:
    def __init__(self):
        self.graph = None

    def create_graph_from_polygon(self, polygon):
        """
        Create a network graph from a given polygon.
        """
        self.graph = ox.graph_from_polygon(polygon, network_type='drive')

    def generate_motorable_path(self, source_point, target_point):
        """
        Generate a motorable path between two points.
        """
        if not self.graph:
            raise ValueError("Graph not initialized. Please create a graph first.")

        source_node = ox.get_nearest_node(self.graph, source_point)
        target_node = ox.get_nearest_node(self.graph, target_point)
        path = nx.shortest_path(self.graph, source_node, target_node)

        return path

    def reverse_geocode(self, address):
        """
        Reverse geocode an address to obtain its coordinates.
        """
        location = ox.geocode(address)
        point = Point(location['lon'], location['lat'])
        
        return point

    def compute_motorable_distance(self, source_point, target_point):
        """
        Compute the motorable distance between two points.
        """
        if not self.graph:
            raise ValueError("Graph not initialized. Please create a graph first.")

        source_node = ox.get_nearest_node(self.graph, source_point)
        target_node = ox.get_nearest_node(self.graph, target_point)
        distance = nx.shortest_path_length(self.graph, source_node, target_node, weight='length')

        return distance

    def plot_graph(self):
        """
        Plot the graph.
        """
        if not self.graph:
            raise ValueError("Graph not initialized. Please create a graph first.")

        fig, ax = ox.plot_graph(self.graph, node_color='b', node_size=30, node_alpha=0.5, edge_color='r')

if __name__ == "__main__":
    # Example usage
    sdk = OpenStreetMapSDK()

    # Define a polygon
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])

    # Create a graph from the polygon
    sdk.create_graph_from_polygon(polygon)

    # Generate a motorable path between two points
    source_point = (0.1, 0.1)
    target_point = (0.9, 0.9)
    path = sdk.generate_motorable_path(source_point, target_point)
    print("Motorable Path:", path)

    # Reverse geocode an address to obtain its coordinates
    address = "New York City, USA"
    point = sdk.reverse_geocode(address)
    print("Reverse Geocoded Point:", point)

    # Compute the motorable distance between two points
    distance = sdk.compute_motorable_distance(source_point, target_point)
    print("Motorable Distance:", distance)

    # Plot the graph
    sdk.plot_graph()
    plt.show()
