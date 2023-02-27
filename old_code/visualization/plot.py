# This file contains functions to plot results.

import matplotlib.pyplot as plt
import networkx as nx
import ast
import numpy as np
import os
import pandas as pd
import seaborn as sns

def plot_local_region(length, width, test_size, shadow_size, data_name, d):
    # used to plot coefficients of Lasso for new algorithm on 2D grid to visualize local region found by algorithm

    q1 = 0
    q2 = 0

    # linear regression file
    #f = open('./../clean_results/test_size=0.5_shadow_size=1000_orig_data_qubits_d=2_linear_regression/coefficients_4x5.txt', 'r')

    # all other files
    f = open('./../clean_results/new_algorithm/test_size={}_shadow_size={}_qubits_d={}/coefficients_{}x{}_{}_data.txt'.format(test_size, shadow_size, d, length, width, data_name), 'r')
    for line in f:
        if line[0:1] == '(':
            q1, q2 = ast.literal_eval(line[11:-1])
        else:
            edge_and_coef = ast.literal_eval(line)
            coef = np.array(list(map(lambda x : x[1], edge_and_coef)))

            G = nx.grid_2d_graph(length, width)

            pos = {(x, y) : (y, -x) for x, y in G.nodes()}
            node_to_int = {}
            for i in range(len(G.nodes())):
                (x, y) = list(G.nodes())[i]
                node_to_int[(x, y)] = i + 1

            edge_cmap = plt.cm.viridis
            line_width = coef * 100
            edge_color = coef * 100
            vmin = min(edge_color)
            vmax = max(edge_color)

            # this is same order as all_edges in algorithm
            edges = list(map(lambda e : (node_to_int[e[0]], node_to_int[e[1]]), list(G.edges())))

            nx.draw_networkx_nodes(
                G,
                pos,
                node_color='#ffffff',
                edgecolors='#000000',
                linewidths=3.5,
                node_size=500)
            nx.draw_networkx_edges(
                G,
                pos,
                edge_cmap=edge_cmap,
                width=line_width,
                edge_color=edge_color,
                edge_vmin=vmin,
                edge_vmax=vmax)

            nx.draw_networkx_labels(
                G,
                pos,
                labels=node_to_int,
                font_family='avenir',
                verticalalignment='center_baseline')

            # creating colorbar
            sm = plt.cm.ScalarMappable(cmap=edge_cmap, norm=plt.Normalize(vmin=vmin/100, vmax=vmax/100))
            sm._A = []
            plt.colorbar(sm)

            ax = plt.gca()
            ax.set_axis_off()
            ax.margins(0.10)

            plt.title('Coefficients of ML Model for (q1, q2) = ({}, {})'.format(q1, q2), fontname='avenir')
            
            # for linear regression test plots
            #plt.savefig('./plots/test_plots_test_size=0.5_shadow_size=1000_orig_data_qubits_d=2_4x5_linear_regression/q1={}_q2={}.png'.format(q1, q2), dpi=300)

            # for other plots
            new_dir = './local_region_plots/test_size={}_shadow_size={}_{}_data_qubits_d={}_{}x{}'.format(test_size, shadow_size, data_name, d, length, width)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            plt.savefig('{}/q1={}_q2={}.png'.format(new_dir, q1, q2), dpi=300)
            plt.clf()
            #plt.show()

    f.close()

if __name__ == '__main__':
    # for plotting local region:
    # length = 4
    # width = 5
    # test_size = 0.5
    # shadow_size = 1000
    # data_name = 'new'
    # d = 1
    # plot_local_region(length, width, test_size, shadow_size, data_name, d)


    # for plotting prediction error:
    sns.set(style="whitegrid")
    df = pd.read_excel('./../clean_results/results.xlsx')

    # only using data where we have both previous method and new method data
    df = df.dropna()

    # for combined 3x3 plots
    # fig, axs = plt.subplots(3, 3, sharey=True, sharex='col', figsize=(15,8))
    
    # for i in range(3):
    #     for j in range(3):
    #         xaxis = ['System Size', 'Training Size', 'Shadow Size']
    #         legend = False
    #         if j == 2 and i == 2:
    #             legend = True
    #         sns.lineplot(
    #             data=df[df['Distance'] == i + 1],
    #             x=xaxis[j],
    #             y='Avg Prediction Error',
    #             style='Training Size',
    #             hue='Algorithm',
    #             marker='o',
    #             ci=None,
    #             ax=axs[i][j],
    #             legend=legend
    #         )
    # axs[0][2].set_title('Distance 1', x=1.2, y=0.4)
    # axs[1][2].set_title('Distance 2', x=1.2, y=0.4)
    # axs[2][2].set_title('Distance 3', x=1.2, y=0.4)

    # axs[0][2].set_xscale('log')
    # axs[0][2].set_xticks([50, 100, 250, 500, 1000])
    # axs[0][2].set_xticklabels([50, 100, 250, 500, 1000])

    # axs[2][2].legend(bbox_to_anchor=(1, 3.5), loc='upper left', ncol=1)

    # for single plots
    sns.relplot(
        kind='line',
        data=df,
        x='System Size',
        y='Avg Prediction Error',
        col='Distance',
        row='Data Set',
        style='Algorithm',
        hue='Algorithm',
        marker='o',
        #col_wrap=3,
        ci=None
    )
    plt.xticks(['4x5', '5x5', '6x5', '7x5', '8x5', '9x5'])

    # for shadow size plots
    # plt.xscale('log')
    # plt.xticks([50, 100, 250, 500, 1000])

    # plt.tight_layout()
    plt.savefig('./prediction_error_plots/test_plots/prediction_error_vs._system_size/algorithm_lines_data_sep.png')

    print('done.')