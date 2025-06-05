import random
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'

def global_efficiency(G):
    if len(G) <= 1:
        return 0
    lengths = dict(nx.all_pairs_shortest_path_length(G))
    total_eff = sum(1 / lengths[u][v] for u in G for v in G if u != v and v in lengths[u])
    return total_eff / (len(G) * (len(G) - 1))

def efficiency_over_removal(G, node_order):
    values = [global_efficiency(G)]
    for i in range(1, len(node_order) + 1):
        G_sub = G.copy()
        G_sub.remove_nodes_from(node_order[:i])
        values.append(global_efficiency(G_sub))
    return values

def load_network_from_excel(path, sheet_name='Sheet1'):
    df = pd.read_excel(path, sheet_name=sheet_name, index_col=0)
    G = nx.DiGraph()
    for i, row in df.iterrows():
        for j, val in row.items():
            if val == 1:
                G.add_edge(i, j)
    return G, list(df.index)

def plot_efficiency_curves(G, node_orders, labels):
    results = [efficiency_over_removal(G, order) for order in node_orders]

    plt.figure(figsize=(8, 6))
    for i, values in enumerate(results):
        plt.plot(range(len(values)), values, marker='o', linestyle='-', label=labels[i])

    plt.xlabel('Number of Removed Nodes', fontsize=16)
    plt.ylabel('Network Efficiency', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2,
               frameon=False, prop={'family': 'Times New Roman', 'size': 14})
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    import os
    file_path = os.path.join(os.getcwd(), 'data.xlsx')
    G, node_names = load_network_from_excel(file_path)

    accident_nodes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    candidate_nodes = [n for n in G.nodes if n not in accident_nodes]
    random_nodes = random.sample(candidate_nodes, min(20, len(candidate_nodes)))

    node_orders = [
        ['E16', 'E15', 'E12', 'H2', 'H3', 'E8', 'E11', 'E6', 'E7', 'H5', 'H1', 'E13', 'E3', 'EN1', 'E14', 'E9', 'EN2', 'E10', 'E1', 'E2'],
        ['E16', 'EN1', 'H5', 'E15', 'E8', 'E12', 'H2', 'H3', 'E14', 'E13', 'EN2', 'E3', 'E6', 'E7', 'E9', 'E11', 'T4', 'H1', 'M5', 'M4'],
        ['H2', 'H3', 'E15', 'H1', 'EN4', 'E14', 'E16', 'E1', 'E2', 'E3', 'EN1', 'EN2', 'E17', 'E11', 'E8', 'M5', 'E6', 'E7', 'M4', 'T1'],
        random_nodes,
        ['M1', 'M5', 'M4', 'M3', 'T5', 'H3', 'T2', 'E3', 'H2', 'E4', 'T3', 'T4', 'H1', 'M2', 'EN2', 'EN4', 'T1', 'E17', 'E2', 'E5']
    ]

    labels = [
        'Degree-based interference',
        'Betweenness-based interference',
        'Closeness-based interference',
        'Random-based interference',
        'Reachability-based interference'
    ]

    plot_efficiency_curves(G, node_orders, labels)
