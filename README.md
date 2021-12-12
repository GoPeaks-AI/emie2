# EMIE 2.0
EMIE 2.0 is a browser-based Python application, written using the [Dash](https://github.com/plotly/dash) framework, that visualizes a knowledge graph. Users can upload their own dataset as input and filter the visualized data. Additionally, the graph can also be downloaded as a jpg.

It uses [networkx](https://github.com/networkx/networkx) to create a graph data structure and visualizes it using [dash-cytoscape](https://github.com/plotly/dash-cytoscape).

The application is hosted at: [https://gopeaks-emie2.herokuapp.com](https://gopeaks-emie2.herokuapp.com)

## Installation
Install all dependencies
```
pip install -r requirements.txt
```

## Usage
Run ```app.py```
```
python app.py
```
The application can now be viewed at [http://localhost:8050](http://localhost:8050).
