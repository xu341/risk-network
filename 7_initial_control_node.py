import random
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

plt.rcParams['font.family'] = 'Times New Roman'

def update_node_status(graph, node, beta, gamma, step, intervention_step):
    status = graph.nodes[node]['status']
    if status == 'C': 
        return
    if status == 'S':
        if any(graph.nodes[neighbor]['status'] == 'I' and random.random() < beta for neighbor in graph.predecessors(node)):
            graph.nodes[node]['status'] = 'I'
    elif status == 'I' and step >= intervention_step and random.random() < gamma:
        graph.nodes[node]['status'] = 'R'

def get_infected_ratio(graph):
    return sum(graph.nodes[n]['status'] == 'I' for n in graph) / graph.number_of_nodes()

def sir_simulation(graph, sources, beta, gamma, steps, intervention_step, control_nodes=None):
    for n in graph:
        graph.nodes[n]['status'] = 'S'
    for src in sources:
        graph.nodes[src]['status'] = 'I'
    if control_nodes:
        for c in control_nodes:
            graph.nodes[c]['status'] = 'C'

    ratios = [get_infected_ratio(graph)]
    for step in range(steps):
        for node in list(graph.nodes):
            update_node_status(graph, node, beta, gamma, step, intervention_step)
        ratios.append(get_infected_ratio(graph))
    return ratios

def apply_control(graph, control_node_indices):
    G = graph.copy()
    for node in control_node_indices or []:
        for neighbor in list(G.predecessors(node)) + list(G.successors(node)):
            G.remove_edge(neighbor, node) if G.has_edge(neighbor, node) else None
            G.remove_edge(node, neighbor) if G.has_edge(node, neighbor) else None
    return G

def plot_sir_by_control_nodes(base_graph, accident_nodes, beta, gamma, steps, intervention_step, node_names, simulations):
    name_to_index = {name: idx for idx, name in enumerate(node_names)}
    x = np.arange(steps + 1)

    control_configs = [
        {'label': 'Control: E16, EN1, H5', 'nodes': ['E16', 'EN1', 'H5']},
        {'label': 'Control: H2, H3, E15', 'nodes': ['H2', 'H3', 'E15']},
        {'label': 'Control: E16, E15, E12', 'nodes': ['E16', 'E15', 'E12']},
        {'label': 'Control: M1, M5, M4', 'nodes': ['M1', 'M5', 'M4']},
        {'label': 'Random Control', 'nodes': None}
    ]

    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for idx, config in enumerate(control_configs):
        all_ratios = np.zeros((simulations, steps + 1))
        random_combos = []

        for sim in range(simulations):
            available_nodes = [n for n in node_names if n not in accident_nodes]
            control_nodes = config['nodes']

            if control_nodes is None:  
                initial_infected = [random.choice(available_nodes)]
                control_candidates = [n for n in available_nodes if n not in initial_infected]
                control_nodes = random.sample(control_candidates, 3)
                random_combos.append(tuple(sorted(control_nodes)))
            else:
                initial_infected = [random.choice([n for n in available_nodes if n not in control_nodes])]

            infected_idx = [name_to_index[n] for n in initial_infected]
            control_idx = [name_to_index[n] for n in control_nodes]
            G_controlled = apply_control(base_graph, control_idx)

            ratios = sir_simulation(G_controlled, infected_idx, beta, gamma, steps, intervention_step, control_idx)
            all_ratios[sim] = ratios

        if config['label'].startswith('Random'):
            most_common = Counter(random_combos).most_common(1)[0][0]
            config['label'] = f"Random Control: {', '.join(most_common)}"

        avg_ratios = np.mean(all_ratios, axis=0)
        plt.plot(x, avg_ratios,
                 label=config['label'],
                 color=default_colors[idx],
                 linestyle='--' if 'Random' in config['label'] else '-')

    plt.xlabel('Step', fontsize=16)
    plt.ylabel('I(s)', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(np.linspace(0.0, 0.4, 5), fontsize=12)
    plt.legend(fontsize=12, loc='upper right')
    plt.tight_layout()

    plt.figtext(0.55, -0.01,
                f'Default parameters: Initial infection node: random, Δs = {intervention_step}, β = {beta}, γ = {gamma}',
                ha='center', fontsize=14)
    plt.figtext(0.5, -0.07, "e) Different initial control nodes", ha='center', fontsize=16)
    plt.show()


if __name__ == '__main__':
    import os
    path = os.path.join(os.getcwd(), 'data.xlsx')
    adj_df = pd.read_excel(path, sheet_name='Sheet1', index_col=0)
    graph = nx.DiGraph(adj_df.values)
    node_names = adj_df.index.to_list()

    accident_nodes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    beta = 0.3
    gamma = 0.3
    steps = 50
    intervention_step = 7
    simulations = 100

    plot_sir_by_control_nodes(graph, accident_nodes, beta, gamma, steps, intervention_step, node_names, simulations)