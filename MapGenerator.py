import networkx as nx
import random
import folium
import webview
from osmnx import graph_from_place, nearest_nodes
from geopy.distance import geodesic
from collections import defaultdict
import osmnx as ox

class OptimalRouteGeneratorMap:
    def __init__(self):
        self.states = [f'q{i}' for i in range(12)]
        self.graphs = []
        self.current_time = 0
        self.max_time = 10  # 10 segundos de simulación
        self.start_point = None
        self.end_point = None
        self.road_graph = None

        # Definir colores para los niveles de tráfico
        self.traffic_colors = {
            'sin_trafico': '#90EE90',    # Verde claro
            'poco_trafico': '#FEEC37',    # Amarillo claro
            'trafico_medio': '#FFB366',   # Naranja claro
            'trafico_alto': '#FF6666'     # Rojo
        }

    def get_node_color(self, weight):
        """Determina el color del nodo según su peso"""
        if 0 <= weight <= 5:
            return self.traffic_colors['sin_trafico']
        elif 5 < weight <= 10:
            return self.traffic_colors['poco_trafico']
        elif 10 < weight <= 15:
            return self.traffic_colors['trafico_medio']
        else:
            return self.traffic_colors['trafico_alto']

    def create_base_graph(self):
        """Crea el grafo base con los 12 estados"""
        G = nx.Graph()
        for state in self.states:
            G.add_node(state, weight=random.randint(1, 10))
        for i in range(len(self.states) - 1):
            G.add_edge(self.states[i], self.states[i + 1])
        return G

    def generate_multiple_graphs(self):
        """Genera entre 1 y 5 grafos diferentes"""
        num_graphs = random.randint(1, 5)
        for _ in range(num_graphs):
            graph = self.create_base_graph()
            self.graphs.append(graph)

    def set_origin_and_destination(self):
        """Genera dos puntos aleatorios en Fusagasugá para el nodo de inicio (q0) y el nodo final (q11)"""
        fusa_location = "Fusagasugá, Colombia"
        self.road_graph = graph_from_place(fusa_location, network_type='drive')

        nodes = list(self.road_graph.nodes)
        # Selección aleatoria de dos nodos diferentes para q0 y q11
        self.start_point = random.choice(nodes)
        self.end_point = random.choice(nodes)
        while self.start_point == self.end_point:
            self.end_point = random.choice(nodes)

    def update_weights_based_on_sequence(self, turing_string):
        """Actualiza los pesos de los nodos según las secuencias encontradas"""
        for graph in self.graphs:
            sequences = {
                2: self.find_sequences(turing_string, 2),
                3: self.find_sequences(turing_string, 3),
                4: self.find_sequences(turing_string, 4)
            }
            if sequences[2]:
                self.update_even_nodes(graph)
            if sequences[3]:
                self.update_odd_nodes(graph)
            if sequences[4]:
                self.update_specific_nodes(graph)
            self.check_weight_limits(graph)

    def find_sequences(self, string, length):
        """Encuentra secuencias de números iguales de longitud específica"""
        sequences = []
        for i in range(len(string) - length + 1):
            if all(string[i] == string[j] for j in range(i, i + length)):
                sequences.append(string[i:i + length])
        return sequences

    def update_even_nodes(self, graph):
        """Incrementa peso de nodos pares en 1"""
        for i in range(0, 12, 2):
            node = f'q{i}'
            graph.nodes[node]['weight'] += 1

    def update_odd_nodes(self, graph):
        """Incrementa peso de nodos impares en 2"""
        for i in range(1, 12, 2):
            node = f'q{i}'
            graph.nodes[node]['weight'] += 2

    def update_specific_nodes(self, graph):
        """Incrementa peso de nodos específicos en 3"""
        specific_nodes = ['q0', 'q3', 'q6', 'q9']
        for node in specific_nodes:
            graph.nodes[node]['weight'] += 3

    def check_weight_limits(self, graph):
        """Verifica que ningún nodo supere el peso máximo de 20"""
        for node in graph.nodes():
            if graph.nodes[node]['weight'] > 20:
                graph.nodes[node]['weight'] = 20

    def visualize_graph_on_map(self):
        """Visualiza los grafos en el mapa de Fusagasugá como rutas alternativas desde q0 a q11"""
        fusa_coord = [4.3369, -74.3630]
        mapa = folium.Map(location=fusa_coord, zoom_start=14, tiles='OpenStreetMap')

        # Agregar nodos de inicio y fin al mapa
        start_latlon = (self.road_graph.nodes[self.start_point]['y'], self.road_graph.nodes[self.start_point]['x'])
        end_latlon = (self.road_graph.nodes[self.end_point]['y'], self.road_graph.nodes[self.end_point]['x'])
        folium.Marker(location=start_latlon, popup="Inicio (q0)", icon=folium.Icon(color='green')).add_to(mapa)
        folium.Marker(location=end_latlon, popup="Destino (q11)", icon=folium.Icon(color='red')).add_to(mapa)

        for i, graph in enumerate(self.graphs):
            # Obtener el camino más corto entre q0 y q11 en el grafo de carreteras
            shortest_path = nx.shortest_path(self.road_graph, source=self.start_point, target=self.end_point, weight='length')
            route_coords = [(self.road_graph.nodes[node]['y'], self.road_graph.nodes[node]['x']) for node in shortest_path]

            # Dibujar la ruta en el mapa
            folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=0.7).add_to(mapa)

            # Agregar nodos con pesos como marcadores en la ruta
            for node in graph.nodes:
                lat, lon = route_coords[self.states.index(node) % len(route_coords)]
                weight = graph.nodes[node]['weight']
                folium.CircleMarker(
                    location=(lat, lon),
                    radius=5,
                    color=self.get_node_color(weight),
                    fill=True,
                    fill_color=self.get_node_color(weight),
                    popup=f"Estado: {node}, Peso: {weight}"
                ).add_to(mapa)

        # Guardar el mapa en un archivo HTML
        mapa_fusa = "mapa_fusa_con_ruta_optima.html"
        mapa.save(mapa_fusa)
        print("Mapa con grafos generado exitosamente como 'mapa_fusa_con_rutas.html'")
        # Mostrar el mapa en una ventana utilizando pywebview
        webview.create_window('Mapa de Fusagasugá con Caminos', mapa_fusa)
        webview.start()

    def generate_optimal_route(self, turing_string):
        """Ejecuta la simulación del autómata celular"""
        self.generate_multiple_graphs()
        self.set_origin_and_destination()
        self.update_weights_based_on_sequence(turing_string)
        self.visualize_graph_on_map()