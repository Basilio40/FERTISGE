# TODO

from .base import ReportGenerator

class HTMLGenerator(ReportGenerator):
    """This is a generator to output a XHTML that uses CSS and best practices
    on standards."""
    filename = None

    def __init__(self, report, filename, *args, **kwargs):
        super(HTMLGenerator, self).__init__(report, *args, **kwargs)

        self.filename = filename

    def execute(self):
        pass

