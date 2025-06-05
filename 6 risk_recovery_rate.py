import random
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'

def update_node_status(graph, node, beta, gamma, step, intervention_step):
    status = graph.nodes[node]['status']
    if status == 'S':
        if any(graph.nodes[neighbor]['status'] == 'I' and random.random() < beta for neighbor in graph.predecessors(node)):
            graph.nodes[node]['status'] = 'I'
    elif status == 'I' and step >= intervention_step and random.random() < gamma:
        graph.nodes[node]['status'] = 'R'

def get_infected_ratio(graph):
    return sum(graph.nodes[n]['status'] == 'I' for n in graph) / graph.number_of_nodes()

def sir_simulation(graph, sources, beta, gamma, steps, intervention_step):
    for n in graph:
        graph.nodes[n]['status'] = 'S'
    for src in sources:
        graph.nodes[src]['status'] = 'I'

    ratios = [get_infected_ratio(graph)]
    for step in range(steps):
        for node in list(graph.nodes):
            update_node_status(graph, node, beta, gamma, step, intervention_step)
        ratios.append(get_infected_ratio(graph))
    return ratios

def plot_sir_by_gamma(graph, source_sets, betas, gammas, steps, intervention_steps, node_names, simulations):
    name_to_index = {name: idx for idx, name in enumerate(node_names)}
    x = np.arange(steps + 1)

    for idx, (sources, beta, gamma, step_point) in enumerate(zip(source_sets, betas, gammas, intervention_steps)):
        infected_indices = [name_to_index[name] for name in sources]
        results = np.zeros((simulations, steps + 1))
        for sim in range(simulations):
            results[sim] = sir_simulation(graph.copy(), infected_indices, beta, gamma, steps, step_point)

        avg_result = np.mean(results, axis=0)
        plt.plot(x, avg_result, label=f'γ = {gamma}')

    plt.xlabel('Step', fontsize=16)
    plt.ylabel('I(s)', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)

    plt.text(-steps * 0.05, -0.2,
             f'Default parameters: Initial infection node: {sources[0]}, ∆s = {intervention_steps[0]}, β = {betas[0]}',
             fontsize=14)
    plt.figtext(0.5, -0.1, "d) Different risk recovery rates", ha='center', fontsize=16)
    plt.show()

if __name__ == '__main__':
    path = 'D:/paper/data.xlsx' # <-- Replace with your own local file path
    adj_df = pd.read_excel(path, sheet_name='Sheet1', index_col=0)
    graph = nx.DiGraph(adj_df.values)
    node_names = adj_df.index.to_list()

    first_i = [['M1']] * 3
    betas = [0.3] * 3
    gammas = [0.2, 0.3, 0.4]
    intervention_steps = [5] * 3
    steps = 50
    simulations = 100

    plot_sir_by_gamma(graph, first_i, betas, gammas, steps, intervention_steps, node_names, simulations)