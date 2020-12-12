import json
import click

from bokeh.server.server import Server

from .data_client import DataClient
from .bokeh_app import BokehApp


@click.command()
@click.option("--uri", required=True, type=str, help="A valid mongoDB uri string")
@click.option("--db", required=True, type=str, help="mongoDB database name")
@click.option("--collection", required=True, type=str, help="mongoDB collection name")
@click.option(
    "--pipeline",
    required=True,
    type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True),
    help="Path to JSON file containg aggregation pipeline",
)
def main(uri: str, db: str, collection: str, pipeline: str) -> None:
    with open(pipeline, "r") as pipeline_file:
        pipeline_json = json.loads(pipeline_file.read())

    data_client = DataClient(
        uri,
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
