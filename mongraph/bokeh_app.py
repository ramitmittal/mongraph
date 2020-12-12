from bokeh.application.application import Application
from bokeh.application.handlers import Handler

from .plot import render


class BokehHandler(Handler):
    def __init__(self, data_client):
        super(BokehHandler, self).__init__()
        self.data_client = data_client

    def modify_document(self, doc):
        nodes = self.data_client.fetch()
        layout = render(nodes)

        doc.title = "Mongraph"
        doc.add_root(layout)


class BokehApp(Application):
    def __init__(self, data_client):
        super(BokehApp, self).__init__()

        bokeh_handler = BokehHandler(data_client)
        self.add(bokeh_handler)
