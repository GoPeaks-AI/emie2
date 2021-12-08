import pandas as pd
from dash import dash_table, dcc
import columns as cols


def make_data_table(df):
    data_table = dash_table.DataTable(
        id="data-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        page_action="native",
        page_current= 0,
        page_size=10,
    )

    return data_table


def make_preds_dropdown(df):
    return dcc.Dropdown(
        id='preds-dropdown',
        options=[{"label" : i, "value" : i} for i in df[cols.ID].unique()],
        value=[],
        placeholder="Select predictors",
        multi=True
    )


def make_outcome_dropdown(df):
    return dcc.Dropdown(
        id='outcome-dropdown',
        options=[{"label" : i, "value" : i} for i in df[cols.OUTCOME].unique()],
        value=[],
        placeholder="Select outcomes",
        multi=True
    )
