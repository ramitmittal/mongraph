from bokeh.application.application import Application
from bokeh.application.handlers import Handler

from .layout_generator import LayoutGenerator


class BokehHandler(Handler):
    def __init__(self, data_client):
        super(BokehHandler, self).__init__()
        self.layout_generator = LayoutGenerator(data_client)

    def modify_document(self, doc):
        layout = self.layout_generator.create_layout()

        doc.title = "Mongraph"
        doc.add_root(layout)


class BokehApp(Application):
    def __init__(self, data_client):
        super(BokehApp, self).__init__()

        bokeh_handler = BokehHandler(data_client)
        self.add(bokeh_handler)
