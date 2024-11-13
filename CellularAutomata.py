import networkx as nx
import random
import time
import matplotlib.pyplot as plt
from collections import defaultdict

class TrafficCellularAutomata:
    def __init__(self):
        self.states = [f'q{i}' for i in range(12)]
        self.graphs = []
        self.current_time = 0
        self.max_time = 10  # 10 segundos de simulación

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
        # Agregar nodos con peso inicial aleatorio
        for state in self.states:
            G.add_node(state, weight=random.randint(1, 10))

        # Conectar nodos
        for i in range(len(self.states)-1):
            G.add_edge(self.states[i], self.states[i+1])

        return G

    def generate_multiple_graphs(self):
        """Genera entre 1 y 5 grafos diferentes"""
        num_graphs = random.randint(1, 5)
        for _ in range(num_graphs):
            graph = self.create_base_graph()
            self.graphs.append(graph)

    def update_weights_based_on_sequence(self, turing_string):
        """Actualiza los pesos de los nodos según las secuencias encontradas"""
        for graph in self.graphs:
            # Buscar secuencias de números iguales
            sequences = {
                2: self.find_sequences(turing_string, 2),
                3: self.find_sequences(turing_string, 3),
                4: self.find_sequences(turing_string, 4)
            }

            # Actualizar pesos según las reglas
            if sequences[2]:  # Secuencias de 2
                self.update_even_nodes(graph)
            if sequences[3]:  # Secuencias de 3
                self.update_odd_nodes(graph)
            if sequences[4]:  # Secuencias de 4
                self.update_specific_nodes(graph)

            # Verificar límite de peso
            self.check_weight_limits(graph)

    def find_sequences(self, string, length):
        """Encuentra secuencias de números iguales de longitud específica"""
        sequences = []
        for i in range(len(string) - length + 1):
            if all(string[i] == string[j] for j in range(i, i + length)):
                sequences.append(string[i:i+length])
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

    def get_graph_weights(self):
        """Calcula el peso total de cada grafo"""
        weights = []
        for graph in self.graphs:
            total_weight = sum(graph.nodes[node]['weight'] for node in graph.nodes())
            weights.append(total_weight)
        return weights

    def visualize_graph(self, graph_index):
        """Visualiza un grafo específico con sus pesos y colores según nivel de tráfico"""
        if graph_index < len(self.graphs):
            graph = self.graphs[graph_index]
            pos = nx.spring_layout(graph)

            plt.figure(figsize=(12, 8))

            # Obtener colores para cada nodo según su peso
            node_colors = [self.get_node_color(graph.nodes[node]['weight'])
                         for node in graph.nodes()]

            # Dibujar el grafo
            nx.draw(graph, pos, with_labels=True,
                   node_color=node_colors,
                   node_size=500, font_size=10,
                   font_weight='bold')

            # Agregar etiquetas de peso
            labels = nx.get_node_attributes(graph, 'weight')
            nx.draw_networkx_labels(graph, pos,
                                  {node: f'{node}\n({weight})'
                                   for node, weight in labels.items()})

            # Agregar leyenda
            legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                        markerfacecolor=color, label=label, markersize=10)
                             for label, color in [
                                 ('Sin tráfico (0-5)', self.traffic_colors['sin_trafico']),
                                 ('Poco tráfico (5-10)', self.traffic_colors['poco_trafico']),
                                 ('Tráfico medio (10-15)', self.traffic_colors['trafico_medio']),
                                 ('Tráfico alto (15-20)', self.traffic_colors['trafico_alto'])
                             ]]
            plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

            plt.title(f'Grafo {graph_index + 1} - Peso Total: {sum(labels.values())}')
            plt.tight_layout()
            plt.show()

    def simulate(self, turing_string):
        """Ejecuta la simulación del autómata celular"""
        self.generate_multiple_graphs()
        start_time = time.time()

        while time.time() - start_time < self.max_time:
            self.update_weights_based_on_sequence(turing_string)
            time.sleep(2)  # Actualización cada 2 segundos

        # Mostrar resultados finales
        weights = self.get_graph_weights()
        min_weight = min(weights) # Encontrar el menor peso
        min_weight_graph = weights.index(min_weight) + 1

        # Imprimir pesos de cada grafo
        for i in range(len(self.graphs)):
            print(f"Grafo {i+1} - Peso total: {weights[i]}")
            self.visualize_graph(i)

        # Imprimir el grafo con menor peso
        print(f"El grafo con menor peso es: Grafo {min_weight_graph} con un peso total de {min_weight}")
