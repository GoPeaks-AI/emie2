import pandas as pd
from dash import dash_table


def make_data_table():
    df = pd.read_csv("data/test.csv")

    data_table = dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        page_action="native",
        page_current= 0,
        page_size=10,
    )

    return df, data_table
