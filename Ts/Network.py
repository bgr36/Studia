import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=np.inf)
x = 1

# funkcja do rysowania grafu sieci
def plot_network(graph):
    plt.clf()
    nx.draw(graph, with_labels=True)
    plt.show()

# funkcja tworząca spójną losową sieć
def create_connected_network(num_nodes, num_edges):
    global x
    edges = []
    nodes = list(range(1,num_nodes+1))
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    np.random.shuffle(nodes)
    
    for i in range(num_nodes - 1):
        edges.append((nodes[i], nodes[i + 1]))
    graph.add_edges_from(edges)
    
    while len(edges) < num_edges:
        u, v = np.random.randint(1, num_nodes, size=2)
        if u != v and not graph.has_edge(u, v):
            graph.add_edge(int(u), int(v))
            edges.append((u, v))
    

    if x == 0:
        plot_network(graph)
        x=1

    return graph

# funkcja usuwająca krawędzie grafu z podanym prawdopodobieństwem
def destroy_network(graph, propability):
    for edge in graph.edges:
        if np.random.random() > propability:
            graph.remove_edge(*edge)
    
    #plot_network(graph)

    return graph

# funkcja tworząca macierz natężeń strumienia pakietów
def generate_flow_intensity_matrix(num_nodes, min_packets = 100, max_packets=10_000):
    N = np.zeros((num_nodes, num_nodes), dtype=int)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            N[i][j] = np.random.randint(min_packets, max_packets)
            N[j][i] = N[i][j]
    return N

# funkcja tworząca macierz przepustowości
def generate_capacity_matrix(graph, capacity):
    num_nodes = len(graph.nodes)
    edges = graph.edges
    C = np.zeros((num_nodes,num_nodes), dtype=int)
    for u, v in edges:
        C[u-1, v-1] =C[v-1, u-1] = capacity* (0.75+np.random.random()/2)
    return C

# funkcja tworząca macierz przepływu
def generate_flow_matrix(graph, flow_intensity_matrix):
    num_nodes = len(graph.nodes)
    A = np.zeros((num_nodes, num_nodes), dtype=int)
    
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            path = nx.shortest_path(graph, source=i+1, target=j+1)  
            path_length = len(path)
            
            for k in range(path_length - 1):
                A[path[k]-1, path[k+1]-1] += flow_intensity_matrix[i][j] 
                A[path[k+1]-1, path[k]-1] += flow_intensity_matrix[i][j]
    return A

def compute_reliability(num_nodes, flow_intensity_matrix, capacity_matrix, flow_matrix, T_max, packet_size = 12000):
    G = np.sum(flow_intensity_matrix)
    total_sum = 0
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            a_val = flow_matrix[i][j]
            c_val = capacity_matrix[i][j]
            if a_val == c_val == 0:
                continue
            cc_val = c_val/packet_size
            if a_val >= cc_val:
                return False
            total_sum += 2*a_val / (cc_val - a_val)
    T =  total_sum/G
    return T < T_max

def run_simulation(num_nodes=20, num_edges=25, p=0.95, T_max =1_000, m = 12_000, min_packets = 50, max_packets = 200, capacity = 104_857_600, num_trials = 1000):
    reliability_results = 0
    failed_due_disconencted = 0
    failed_due_overload = 0
    # StartingNetwork = create_connected_network(num_nodes, num_edges)

    for i in range(num_trials):
        network = create_connected_network(num_nodes, num_edges)
        network = destroy_network(network, p)
        if not nx.is_connected(network):
            failed_due_disconencted += 1
            continue
        flow_intensity_matrix = generate_flow_intensity_matrix(num_nodes, min_packets, max_packets)
        capacity_matrix = generate_capacity_matrix(network, capacity)
        flow_matrix = generate_flow_matrix(network, flow_intensity_matrix)
        reliability_results+= compute_reliability(num_nodes, flow_intensity_matrix, capacity_matrix, flow_matrix, T_max, m)
        
        # if i == 0:
        #     print(flow_intensity_matrix)
        #     print(capacity_matrix)
        #     print(flow_matrix)
    return float(reliability_results/num_trials), failed_due_disconencted, int(num_trials-reliability_results-failed_due_disconencted)



if __name__ == "__main__":
    # punkt wyjścia
    print("Wartosci podstawowe:\n|V| = 20, |E| = 25, p = 0.95, T_max = 1 000, m = 12 000, min_packets = 50, max_packets = 200, capacity = 100 Mbps")
    print(f"Symulacja standardowa: {run_simulation()}")

    # zwiększamy macierz natężeń
    print("Symulacje przy zwiekszaniu wartosci w macierzy natezen\nZwiekszamy min_packets i max_packets o 10% z kazdym krokiem")
    for i in range(10):
        print(run_simulation(min_packets=50*(1+i/10), max_packets=200*(1+i/10)))

    print("Symulacje przy zwiekszaniu przepustowosci\nZwiekszamy capacity o 10% z kazdym krokiem")
    for i in range(10):
        print(run_simulation(capacity=104_857_600*(1+i/10)))

    print("Symulacje przy zwiekszaniu liczby krawedzi\nZwiekszamy liczbe krawedzi od 20 do 29")
    for i in range(10):
        print(run_simulation(num_edges=20+i))
# pakiet ~ 1500 bajtów = 12000 bitów
# przepustowość ~ 100 Mbps ~ 100 * 10^6 bitów
# liczba pakietów ~ 100-250 pakietów