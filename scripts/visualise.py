import networkx as nx
import matplotlib.pyplot as plt


def visualise_graph(securities, top_n=None, include_other=False):
    G = nx.Graph()
    
    # Filter out 'Other' if not included
    if not include_other:
        securities = [sec for sec in securities if sec.name != "Other"]

    # Sort securities by their weighting in descending order
    securities.sort(key=lambda x: x.weighting, reverse=True)

    # Limit the number of securities to display if top_n is specified
    if top_n is not None:
        securities = securities[:top_n]

    # Add nodes and edges for securities and their corresponding funds
    for security in securities:
        # Add a node for each security
        G.add_node(security.name, size=security.weighting*10)  # Adjust size scaling as needed
        
        # Add nodes for funds and edges between securities and funds
        for fund in security.funds:
            fund_node = f"F:{fund}"
            G.add_node(fund_node)  # Add a node for the fund
            G.add_edge(security.name, fund_node)  # Add an edge between the security and the fund

    # Position nodes using the Kamada-Kawai layout for better visual appearance
    pos = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(15, 10))  # Set the size of the figure

    # Draw nodes with dynamic sizing and labels for securities
    node_sizes = [G.nodes[n]['size'] for n in G.nodes if not n.startswith("F:")]
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if not n.startswith("F:")],
                           node_size=node_sizes, node_color='skyblue', label='Securities')
    nx.draw_networkx_labels(G, pos, labels={n: n for n in G.nodes if not n.startswith("F:")}, font_size=8)

    # Draw nodes and labels for funds
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if n.startswith("F:")],
                           node_size=300, node_color='lightgreen', label='Funds')
    nx.draw_networkx_labels(G, pos, labels={n: n for n in G.nodes if n.startswith("F:")}, font_size=8)

    # Draw edges
    nx.draw_networkx_edges(G, pos)

    plt.title("Securities and Their Funds")
    plt.axis('off')  # Turn off the axis
    plt.legend()  # Show legend
    plt.tight_layout()
    plt.show(block=True)


def visualise_holdings(securities, top_n=None, include_other=False):
    # Filter out 'Other' if not included
    if not include_other:
        securities = [sec for sec in securities if sec.name != "Other"]

    # Sort securities by their weighting in descending order
    securities.sort(key=lambda x: x.weighting, reverse=True)

    # Limit the number of securities to display if top_n is specified
    if top_n is not None:
        securities = securities[:top_n]

    # Prepare data for plotting
    names = [sec.name for sec in securities]
    weightings = [sec.weighting for sec in securities]

    # Create the bar chart
    plt.figure(figsize=(10, 8))
    plt.barh(names, weightings, color='skyblue')
    plt.xlabel('Weighted Average (%)')
    plt.ylabel('Securities')
    plt.title('Top Securities by Weighted Average')
    plt.gca().invert_yaxis()  # Invert y-axis to have the largest on top
    plt.tight_layout()
    plt.show(block=True)