import random
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'

def update_node_status(graph, node, beta, gamma, step, intervention_step):
    status = graph.nodes[node]['status']
    if status == 'S':
        if any(graph.nodes[neighbor]['status'] == 'I' and random.random() < beta
               for neighbor in graph.predecessors(node)):
            graph.nodes[node]['status'] = 'I'
    elif status == 'I' and step >= intervention_step and random.random() < gamma:
        graph.nodes[node]['status'] = 'R'

def count_infected_ratio(graph):
    return sum(graph.nodes[n]['status'] == 'I' for n in graph) / graph.number_of_nodes()

def SIR_simulation(graph, sources, beta, gamma, steps, intervention_step):
    for n in graph:
        graph.nodes[n]['status'] = 'S'
    for src in sources:
        graph.nodes[src]['status'] = 'I'
    
    infected_ratios = [count_infected_ratio(graph)]
    for step in range(steps):
        for node in list(graph.nodes):
            update_node_status(graph, node, beta, gamma, step, intervention_step)
        infected_ratios.append(count_infected_ratio(graph))
    return infected_ratios

def plot_simulation(graph, source_sets, betas, gammas, steps, intervention_steps, node_names, simulations):
    name_to_index = {name: idx for idx, name in enumerate(node_names)}
    x = np.arange(steps + 1)

    for idx, (sources, beta, gamma, step_point) in enumerate(zip(source_sets, betas, gammas, intervention_steps)):
        initial_nodes = [name_to_index[name] for name in sources]
        all_results = np.zeros((simulations, steps + 1))
        for sim in range(simulations):
            all_results[sim] = SIR_simulation(graph.copy(), initial_nodes, beta, gamma, steps, step_point)

        avg_results = np.mean(all_results, axis=0)
        label = f'Random Infection: {sources[0]}' if idx == len(source_sets) - 1 else f'Infection: {sources[0]}'
        linestyle = '--' if idx == len(source_sets) - 1 else '-'
        plt.plot(x, avg_results, linestyle=linestyle, label=label)

    plt.xlabel('Step', fontsize=16)
    plt.ylabel('I(s)', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.text(steps * 0.1, -0.2,
             f'Default parameters: ∆s = {intervention_steps[0]}, β = {betas[0]}, γ = {gammas[0]}',
             fontsize=14)
    plt.figtext(0.5, -0.1, "a) Different initial infection nodes", ha='center', fontsize=16)
    plt.show()

if __name__ == '__main__':
    path = 'D:/paper/data.xlsx' # <-- Replace with your own local file path
    adj_df = pd.read_excel(path, sheet_name='Sheet1', index_col=0)
    graph = nx.DiGraph(adj_df.values)
    node_names = adj_df.index.to_list()

    accident_nodes = {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'M1', 'M4', 'M5'}
    candidates = [n for n in node_names if n not in accident_nodes]
    first_i = [['M1'], ['M4'], ['M5'], [random.choice(candidates)]]

    betas = [0.3] * 4
    gammas = [0.3] * 4
    intervention_steps = [5] * 4
    steps = 50
    simulations = 100

    plot_simulation(graph, first_i, betas, gammas, steps, intervention_steps, node_names, simulations)