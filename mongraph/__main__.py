import json
import click

from bokeh.application.application import Application
from bokeh.application.handlers import Handler
from bokeh.server.server import Server

from .data_client import DataClient
from .plot import render


class BokehHandler(Handler):
    def __init__(self, data_client):
        super(BokehHandler, self).__init__()
        self.data_client = data_client

    def modify_document(self, doc):
        nodes = self.data_client.fetch()
        plot = render(nodes)

        doc.title = "Mongraph"
        doc.add_root(plot)


class BokehApp(Application):
    def __init__(self, data_client):
        super(BokehApp, self).__init__()

        bokeh_handler = BokehHandler(data_client)
        self.add(bokeh_handler)


@click.command()
@click.option(
    "--connection", required=True, type=str, help="A valid mongoDB connection string"
)
@click.option("--db", required=True, type=str, help="mongoDB database name")
@click.option("--collection", required=True, type=str, help="mongoDB collection name")
@click.option(
    "--pipeline",
    required=True,
    type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True),
    help="Path to JSON file containg aggregation pipeline",
)
def main(connection: str, db: str, collection: str, pipeline: str) -> None:
    with open(pipeline, "r") as pipeline_file:
        pipeline_json = json.loads(pipeline_file.read())

    data_client = DataClient(
        connection,
        db,
        collection,
        pipeline_json,
    )

    bokeh_app = BokehApp(data_client)

    server = Server({"/": bokeh_app})
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()


if __name__ == "__main__":
    main()
