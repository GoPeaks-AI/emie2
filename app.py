from dash import Dash, html
from components import data, graph

app = Dash(__name__)
server = app.server

# Components
input_header = html.H2("Knowledge Graph Input")
output_header = html.H2("Knowledge Graph Output")
df, data_table = data.make_data_table()
viz = graph.visualize_graph(df)

app.layout = html.Div([
        input_header,
        data_table,
        output_header,
        viz,
    ])


if __name__ == "__main__":
    app.run_server()
