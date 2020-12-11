import networkx as nx

from bokeh.models import (
    Circle,
    HoverTool,
    MultiLine,
)
from bokeh.palettes import Inferno6
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
    plot.axis.visible = False

    plot.add_tools(HoverTool(tooltips=attribute_list))

    graph = from_networkx(G, nx.spring_layout, scale=5, center=(0, 0))

    graph.node_renderer.glyph = Circle(size=15, fill_color=Inferno6[1], fill_alpha=0.6)
    graph.node_renderer.hover_glyph = Circle(
        size=15, fill_color=Inferno6[4], fill_alpha=0.6
    )
    graph.edge_renderer.glyph = MultiLine(
        line_color=Inferno6[0], line_alpha=0.3, line_width=3
    )

    plot.renderers.append(graph)

    return plot
