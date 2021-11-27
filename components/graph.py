import networkx as nx
import dash_cytoscape as cyto


# Column names
ID = "id"
OUTCOME = "outcome"
CORRELATION = "correlation"
WEIGHT = "weight"


def init_graph(df):
    # rename rescaled weight to weight for ease of use
    df = df.rename(columns={"rescaled weight" : WEIGHT})
    Graphtype = nx.DiGraph()
    G = nx.from_pandas_edgelist(
            df,
            ID,
            OUTCOME,
            edge_attr=[CORRELATION, WEIGHT],
            create_using=Graphtype)

    return G


# Converting networkx data into cytoscape format
def convert_nx_to_cyto(G):
    pos = nx.circular_layout(G)
    cy = nx.readwrite.json_graph.cytoscape_data(G)

    # Create node labels for cytoscape
    for n in cy["elements"]["nodes"]:
        for k,v in n.items():
            v["label"] = v.pop("value")
    
    # Add the node positions as a value for data in the nodes portion of cy
    for n,p in zip(cy["elements"]["nodes"],pos.values()):
        n["pos"] = {"x":p[0],"y":p[1]}
      
    # Combine the dicts of nodes and edges to generate a list
    elements = cy["elements"]["nodes"] + cy["elements"]["edges"]

    return elements


def visualize_graph(df):
    G = init_graph(df)
    elements = convert_nx_to_cyto(G)
    cytoscape = cyto.Cytoscape(
            id="cytoscape",
            layout={ "name" : "circle" },
            elements=elements,
            style={"width": "100%", "height": "600px"},
            minZoom=0.8,
            maxZoom=1,
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "content": "data(label)"
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "width": "data(weight)"
                    }
                },
                {
                    "selector": "[correlation < 0]",
                    "style": {
                        "mid-target-arrow-color": "#f92411",
                        "mid-target-arrow-shape": "triangle-backcurve",
                        "arrow-scale": "1.5",
                        "line-color": "#f92411"
                    }
                },
                {
                    "selector": "[correlation > 0]",
                    "style": {
                        "mid-target-arrow-color": "#61bbfc",
                        "mid-target-arrow-shape": "triangle-backcurve",
                        "arrow-scale": "1.5",
                        "line-color": "#61bbfc"
                    }
                },    
            ]
        )

    return cytoscape
