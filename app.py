import base64
import io

from dash import Dash, html, dcc, dependencies, no_update
from dash.exceptions import PreventUpdate
from components import data, graph
import pandas as pd
import columns as cols


app = Dash(__name__, title="EMIE 2.0 - Knowledge Graph Visualization")
server = app.server


# Load dataset
df = pd.read_csv("data/dataset.csv")


# Components
input_header = html.H2("Knowledge Graph Input")
upload_button = dcc.Upload(
        id="upload-data",
        children=html.Button(className="button", children="Upload CSV")
    )
upload_result = html.Div(id="upload-result")
output_header = html.H2("Knowledge Graph Output")
data_table = data.make_data_table(df)

G = graph.init_graph(df)
elements = graph.convert_nx_to_cyto(G)
viz = graph.visualize_graph(elements)

export_button = html.Button(id="export", className="button", children="Download JPG")
footer = html.Footer(
            className="footer",
            children="Developed by Sharad Swaminathan (sswamin5@uncc.edu) at the University of North Carolina at Charlotte, EMIE2.0 is built in Python for curating and visualizing relationship knowledge data, with a preloaded data of meta-analytic findings of drivers for organizational performance outcomes. This is a product of the GoPeaks Initiative. All copyrights are reserved."
        )

app.layout = html.Div(children=[
        html.Div(className="navbar", children=[
            html.Img(src="/assets/logo.png"),
            html.Span(className="navbar-text", children="EMIE 2.0")
        ]),
        html.Div(className="container", children=[
        input_header,
        html.P(children=[
            "You may upload your own input file to generate a knowledge graph. Make sure it is a csv file with the following columns: ",
            html.B("id, outcome, correlation, significance, number of samples, relative weight, rescaled weight")
        ]),
        upload_result,
        upload_button,
        html.Div([
            html.H3("Select predictors"),
            html.Div(
                id="preds-div",
                children=data.make_preds_dropdown(df)
            )
        ]),
        html.Div([
            html.H3("Select outcomes"),
            html.Div(
                id="outcomes-div",
                children=data.make_outcome_dropdown(df)
            )
        ]),
        html.Div(id="table-div", children=data_table),
        output_header,
        html.Div(id="export-div", children=export_button),
        html.Div(id="graph-div", children=viz)]),
        footer,
        dcc.Store(id="data-store"),
        dcc.Store(id="graph-store")
    ])


# Callback for file upload and update components
@app.callback(
        dependencies.Output("upload-result", "children"),
        dependencies.Output("data-store", "data"),
        dependencies.Output("graph-store", "data"),
        dependencies.Output("table-div", "children"),
        dependencies.Output("graph-div", "children"),
        dependencies.Output("preds-div", "children"),
        dependencies.Output("outcomes-div", "children"),
        dependencies.Input("upload-data", "contents"),
        dependencies.State("upload-data", "filename"),
        prevent_initial_call=True
    )
def update_data(content, filename):
    if content is None:
        raise PreventUpdate
    content_type, content_string = content.split(",")
    decoded = base64.b64decode(content_string)

    error = html.P(className="red-text", children="Invalid input. Make sure you upload a CSV file with the necessary columns.")
    success = html.P("File uploaded: {}".format(filename))
    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            # validate columns
            if not set([
                cols.ID, 
                cols.OUTCOME, 
                cols.CORRELATION,
                cols.SIGNIFICANCE,
                cols.REL_WEIGHT,
                cols.RESCALED_WEIGHT]).issubset(df.columns):
                
                return error, no_update, no_update, no_update, no_update, no_update, no_update
        else:
            return error, no_update, no_update, no_update, no_update, no_update, no_update
    except Exception as e:
        return error, no_update, no_update, no_update, no_update, no_update, no_update

    data_table = data.make_data_table(df)
    G = graph.init_graph(df)
    elements = graph.convert_nx_to_cyto(G)
    viz = graph.visualize_graph(elements)
    preds = data.make_preds_dropdown(df)
    outcomes = data.make_outcome_dropdown(df)

    return success, df.to_dict("records"), elements, data_table, viz, preds, outcomes


# Callback for filtering data
@app.callback(
        dependencies.Output("data-table", "data"),
        dependencies.Output("knowledge-graph", "elements"),
        [dependencies.Input("preds-dropdown", "value")],
        [dependencies.Input("outcome-dropdown", "value")],
        dependencies.State("data-store", "data"),
        dependencies.State("graph-store", "data"),
        prevent_initial_call=True
    )
def filter_data(preds, outcomes, data, graph_data):
    if data and graph_data:
        current_df = pd.DataFrame.from_dict(data)
        current_elems = graph_data
    else:
        current_df = df
        current_elems = elements
    if preds == [] and outcomes == []:
        return current_df.to_dict("records"), current_elems

    filtered_df = current_df.copy()
    hidden_nodes = []
    if preds != []:
        filtered_df = filtered_df[filtered_df[cols.ID].isin(preds)]
        hidden_nodes += current_df[~current_df[cols.ID].isin(preds)][cols.ID].tolist()
    if outcomes != []:
        filtered_df = filtered_df[filtered_df[cols.OUTCOME].isin(outcomes)]
        hidden_nodes += current_df[~current_df[cols.OUTCOME].isin(outcomes)][cols.OUTCOME].tolist()

    def filter_graph(obj):
        if "id" in obj["data"]:
            if obj["data"]["id"] in hidden_nodes:
                return False
            else:
                return True
        elif "source" in obj["data"]:
            if obj["data"]["source"] in hidden_nodes or obj["data"]["target"] in hidden_nodes:
                return False
            else:
                return True

    filtered_elems = list(filter(filter_graph, current_elems))

    return filtered_df.to_dict("records"), filtered_elems


# Callback for exporting graph
@app.callback(
        dependencies.Output("knowledge-graph", "generateImage"),
        dependencies.Input("export", "n_clicks"),
        prevent_initial_call=True
    )
def export_graph(btn_click):
    return {
            "type": "jpg",
            "action": "download"
        }


if __name__ == "__main__":
    app.run_server()
