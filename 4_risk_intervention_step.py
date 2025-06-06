import random
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'

def update_node_status(graph, node, beta, gamma, step, intervention_step):
    status = graph.nodes[node]['status']
    if status == 'S':
        if any(graph.nodes[n]['status'] == 'I' and random.random() < beta for n in graph.predecessors(node)):
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

def plot_sir_by_intervention(graph, infected_node, betas, gammas, steps, intervention_steps, node_names, simulations):
    name_to_index = {name: idx for idx, name in enumerate(node_names)}
    x = np.arange(steps + 1)
    node_idx = [name_to_index[infected_node]]

    for beta, gamma, step_point in zip(betas, gammas, intervention_steps):
        results = np.zeros((simulations, steps + 1))
        for sim in range(simulations):
            results[sim] = sir_simulation(graph.copy(), node_idx, beta, gamma, steps, step_point)
        avg_result = np.mean(results, axis=0)
        plt.plot(x, avg_result, label=f'∆s = {step_point}')

    plt.xlabel('Step', fontsize=16)
    plt.ylabel('I(s)', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(np.arange(0, 0.9, 0.1), fontsize=12)
    plt.legend(fontsize=12)

    plt.text(-steps * 0.05, -0.22,
             f'Default parameters: Initial infection node: {infected_node}, β = {betas[0]}, γ = {gammas[0]}',
             fontsize=14)
    plt.figtext(0.5, -0.1, "b) Different risk intervention steps", ha='center', fontsize=16)
    plt.show()

if __name__ == '__main__':
    import os
    path = os.path.join(os.getcwd(), 'data.xlsx')
    adj_df = pd.read_excel(path, sheet_name='Sheet1', index_col=0)
    graph = nx.DiGraph(adj_df.values)
    node_names = adj_df.index.to_list()

    infected_node = 'M1'
    betas = [0.3] * 3
    gammas = [0.3] * 3
    intervention_steps = [3, 5, 7]
    steps = 50
    simulations = 100

    plot_sir_by_intervention(graph, infected_node, betas, gammas, steps, intervention_steps, node_names, simulations)