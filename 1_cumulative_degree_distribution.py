import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 20

import os
file_path = os.path.join(os.getcwd(), 'data.xlsx')

df = pd.read_excel(file_path, sheet_name='Sheet1', index_col=0)

G = nx.DiGraph()
for i, row in df.iterrows():
    for j, val in row.items():
        if val == 1:
            G.add_edge(i, j)

degrees = [d for _, d in G.degree()]
degree_counts = np.bincount(degrees)
cumulative_distribution = np.cumsum(degree_counts[::-1])[::-1]
cumulative_distribution = cumulative_distribution / cumulative_distribution[0]  


def power_law(x, C, gamma):
    return C * x**(-gamma)

x = np.arange(1, len(cumulative_distribution) + 1)
y = cumulative_distribution

popt, _ = curve_fit(power_law, x, y)
fitted = power_law(x, *popt)

residuals = y - fitted
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y - np.mean(y))**2)
r_squared = 1 - ss_res / ss_tot


plt.figure(figsize=(8, 6))
plt.loglog(x - 1, y, 'o', label='Data')  

plt.xlabel('Log(Degree)', fontsize=16)
plt.ylabel('Log(P(k))', fontsize=16)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.gca().xaxis.set_ticks_position('top')
plt.gca().xaxis.set_label_position('top')
plt.axhline(y=0.1, color='gray', linestyle='--')

plt.text(0.1, 0.8, rf'$P(k) = {popt[0]:.4f} \cdot k^{{-{popt[1]:.4f}}}$', transform=plt.gca().transAxes, fontsize=15)
plt.text(0.1, 0.7, rf'$R^2 = {r_squared:.4f}$', transform=plt.gca().transAxes, fontsize=15)

plt.grid(False)
plt.tight_layout()
plt.show()