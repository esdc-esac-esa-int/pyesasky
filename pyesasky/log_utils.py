# log_utils.py
import logging
import ipywidgets as widgets
from IPython.display import display

# Global logger instance
logger = logging.getLogger('pyesasky_logger')
logger.setLevel(logging.CRITICAL)

class OutputStreamHandler(logging.Handler):
    """Custom logging handler to output logs to an ipywidgets Output widget."""

    def __init__(self, output_widget):
        super().__init__()
        self.output_widget = output_widget

    def emit(self, record):
        try:
            msg = self.format(record)
            with self.output_widget:
                print(msg)
        except Exception:
            self.handleError(record)


def setup_notebook_logging(log_level, output_widget=None, log_to_file=False, file_name="logs.txt"):
    """
    Set up logging for a Jupyter notebook. Optionally log to a file.

    Args:
    - output_widget (ipywidgets.Output): Widget to display logs in the notebook.
    - log_to_file (bool): If True, logs will also be saved to a file.
    - file_name (str): Name of the log file (only if log_to_file is True).

    Returns:
    - logger (logging.Logger): Configured logger.
    """

    logger.setLevel(log_level)

    # Console logging to the notebook Output widget
    if output_widget:
        handler = OutputStreamHandler(output_widget)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Optionally log to a file
    if log_to_file:
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def setup_accordion_logging(log_level):
    """
    Set up logging with an Accordion widget for displaying logs in a collapsible section.

    Returns:
    - logger (logging.Logger): Configured logger with accordion-based log display.
    """
    # Create an output widget
    log_output = widgets.Output()

    # Create a collapsible section for logs
    log_section = widgets.Accordion(children=[log_output])
    log_section.set_title(0, "Logs")

    # Display the log section
    display(log_section)

    # Set up the logger with the Output widget
    logger = setup_notebook_logging(log_level, output_widget=log_output)

    return logger, log_section
