import networkx as nx

from bokeh.core.enums import Align
from bokeh.layouts import column
from bokeh.models import (
    Button,
    Circle,
    HoverTool,
    MultiLine,
)
from bokeh.palettes import Inferno6
from bokeh.plotting import figure, from_networkx


class LayoutGenerator:
    def __init__(self, data_client):
        self.data_client = data_client

    def create_networkx_graph(self, nodes):
        attribute_keys = set()

        # networkx graph is named G for consistency with networkx docs
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

    def create_graph_render(self, G):
        graph = from_networkx(G, nx.spring_layout, scale=5, center=(0, 0))

        graph.node_renderer.glyph = Circle(
            size=15, fill_color=Inferno6[1], fill_alpha=0.6
        )
        graph.node_renderer.hover_glyph = Circle(
            size=15, fill_color=Inferno6[4], fill_alpha=0.6
        )
        graph.edge_renderer.glyph = MultiLine(
            line_color=Inferno6[0], line_alpha=0.3, line_width=3
        )
        return graph

    def create_layout(self):
        nodes = self.data_client.fetch()
        (G, attribute_list) = self.create_networkx_graph(nodes)

        scale = len(nodes)
        plot = figure(
            title="Aggregation results",
            x_range=(-scale, scale),
            y_range=(-scale, scale),
        )
        plot.axis.visible = False

        graph_renderer = self.create_graph_render(G)
        plot.renderers.append(graph_renderer)

        plot.add_tools(HoverTool(tooltips=attribute_list))

        def refresh():
            """on_click handler for the refresh button"""

            nodes = self.data_client.fetch()
            (G, _) = self.create_networkx_graph(nodes)

            new_graph_renderer = self.create_graph_render(G)
            plot.renderers.pop()
            plot.renderers.append(new_graph_renderer)

            # hover tool needs to be re-added to make it work with updated data
            plot.tools = [
                tool for tool in plot.tools if not isinstance(tool, HoverTool)
            ]
            plot.add_tools(HoverTool(tooltips=attribute_list))

        button = Button(label="Refresh", max_width=200, align=Align.center)
        button.on_click(refresh)

        layout = column(plot, button)
        return layout
