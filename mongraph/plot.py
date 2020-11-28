import networkx as nx

from bokeh.models import (
    Circle,
    HoverTool,
    MultiLine,
    TapTool,
)
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, from_networkx


def create_graph(nodes):
    attribute_keys = set()

    G = nx.DiGraph()
    G.add_nodes_from([(node["id"], node["attributes"]) for node in nodes])

    for node in nodes:
        G.add_edges_from(
            [
                (node["id"], other_id)
                for other_id in node["connectsTo"]
                if other_id is not None
            ]
        )
        for key, _ in node["attributes"].items():
            attribute_keys.add(key)

    attribute_list = [(x, f"@{x}") for x in attribute_keys]

    return (G, attribute_list)


def render(nodes):
    (G, attribute_list) = create_graph(nodes)

    scale = len(nodes)
    plot = figure(
        title="Aggregation results",
        x_range=(-scale, scale),
        y_range=(-scale, scale),
    )
    plot.add_tools(HoverTool(tooltips=attribute_list), TapTool())

    graph = from_networkx(G, nx.spring_layout, scale=5, center=(0, 0))

    graph.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])
    graph.edge_renderer.glyph = MultiLine(
        line_color="#CCCCCC", line_alpha=0.8, line_width=5
    )

    plot.renderers.append(graph)

    return plot
