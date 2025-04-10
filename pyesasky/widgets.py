import re
import logging
import requests
import pkg_resources

import ipywidgets as widgets
from ipywidgets import register
from traitlets import Unicode, default, List
from ipyfilechooser import FileChooser
from IPython.display import display, HTML, Javascript


from pyesasky.kernel_comm import KernelComm
from pyesasky.log_utils import setup_accordion_logging, logger
from pyesasky.exceptions import CommNotInitializedError
from pyesasky.message_utils import create_message_output, create_message_result
from pyesasky.api_interactions import ApiInteractionsMixin
import pyesasky.constants as const
from ._version import __version__  # noqa

__all__ = ["ESASkyWidget"]


@register
class ESASkyWidget(widgets.DOMWidget, ApiInteractionsMixin):

    _view_name = Unicode("IFrameView").tag(sync=True)
    _model_name = Unicode("IFrameModel").tag(sync=True)
    _view_module = Unicode("pyesasky").tag(sync=True)
    _model_module = Unicode("pyesasky").tag(sync=True)
    _view_module_version = Unicode(__version__).tag(sync=True)
    _model_module_version = Unicode(__version__).tag(sync=True)
    _view_language = Unicode("En").tag(sync=True)
    _view_module_ids = List().tag(sync=True)
    view_height = Unicode("800px").tag(sync=True)

    def __init__(self, lang="en", enable_logs=False, log_level=logging.DEBUG):
        super().__init__()
        self.kernel_comm = KernelComm(self.comm, self._handle_comm_message)

        if enable_logs:
            setup_accordion_logging(log_level)

        allowed_lang = ["en", "es", "zh"]
        if lang.lower() in allowed_lang:
            self._view_language = lang
        else:
            allowed_lang_str = ", ".join(allowed_lang)
            raise ValueError(
                f"Wrong language code used. Available languages are {allowed_lang_str}"
            )

        self._check_server_version()

        self.modal = DownloadModal()
        self.modal.display()

        self.spinner = SpinnerWidget()
        self.spinner.display()

    def set_view_height(self, height):
        """Sets the widget view height in pixels"""

        height = str(height)
        if not height.endswith("px"):
            height = height + "px"
        self.view_height = height

    def _check_server_version(self):
        version_resp = requests.get(
            "https://pypi.org/rss/project/pyesasky/releases.xml", timeout=self.message_timeout
        )
        if version_resp.status_code != 200:
            return

        match = re.search(r'<title>(\d+\.\d+\.\d+)</title>', version_resp.text)
        installed_version = pkg_resources.get_distribution("pyesasky").version
        if match:
            latest_version = match.group(1)
            if installed_version != latest_version:
                display(HTML(const.VERSION_WARNING_HTML))

    def _handle_comm_message(self, msg_type, content):
        logger.debug("recieved comm message of type: %s", msg_type)
        try:
            self.spinner.show()
            if msg_type == const.MESSAGE_TYPE_DOWNLOAD:
                url = content.get("url")
                response = requests.get(
                    url.strip(), allow_redirects=True, timeout=self.message_timeout
                )

                if response.status_code == 200:
                    logger.debug("File fetched successfully")
                    self.modal.show(response)
                else:
                    logger.debug("Failed to fetch file")
        except Exception:  # noqa
            logger.error(("Error processing comm message"))
        finally:
            self.spinner.hide()

    @default("layout")
    def _default_layout(self):
        return widgets.Layout(height="400px", align_self="stretch")

    def _send_ignore(self, content):
        try:
            self.kernel_comm.send_message(content)
        except CommNotInitializedError:
            return "Communication could not be established"

    def _send_receive(self, content):
        try:
            comm_id = self.kernel_comm.send_message(content)
            resp = self.kernel_comm.wait_message(comm_id, self.message_timeout)

            output = create_message_output(resp)
            if output:
                print(output)

            return create_message_result(resp)
        except TimeoutError:
            return "Timed out waiting for response. Please try again"
        except CommNotInitializedError:
            return "Communication could not be established"


class DownloadModal:
    def __init__(self):
        self.response = None

        self.fc = FileChooser(
            title="Select directory for download",
            show_only_dirs=True,
            dir_icon_append=True,
            select_default=True,
        )

        # Create widgets for modal components
        self.overlay = widgets.Box(
            [],
            layout=widgets.Layout(
                position="fixed",
                top="0",
                left="0",
                width="100%",
                height="100%",
                background_color="rgba(0, 0, 0, 0.5)",
                justify_content="center",
                align_items="center",
                display="none",
                z_index="1000",
            ),
        )
        self.modal_container = widgets.VBox(
            [],
            layout=widgets.Layout(
                background_color="white",
                padding="20px",
                border_radius="8px",
                text_align="center",
                box_shadow="0px 4px 8px rgba(0,0,0,0.2)",
            ),
        )

        self.save_button = widgets.Button(
            description="Save",
            button_style="danger",
            layout=widgets.Layout(width="80px"),
        )
        self.close_button = widgets.Button(
            description="Cancel",
            button_style="danger",
            layout=widgets.Layout(width="80px"),
        )

        self.buttons_row = widgets.HBox(
            [self.save_button, self.close_button],
            layout=widgets.Layout(justify_content="flex-start"),
        )
        # Assemble the modal
        self.modal_container.children = [self.fc, self.buttons_row]
        self.overlay.children = [self.modal_container]

        # Attach event handlers
        self.save_button.on_click(
            lambda _: (
                self._save_file(self.response)
                if self.response
                else logger.warning("No content to save")
            )
        )
        self.close_button.on_click(self.hide)

    def _save_file(self, response):
        if self.fc.selected is not None:
            try:
                file_name = self._extract_file_name(response)
                content = response.content
                with open(f"{self.fc.selected}/{file_name}", "wb") as f:
                    f.write(content)
            except (AttributeError, KeyError) as e:
                logger.error(f"Attribute error or missing key: {e}")
            except FileNotFoundError as e:
                logger.error(f"File path not found: {e}")
            except OSError as e:
                logger.error(f"Error opening/writing the file: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")

        self.hide()

    def _extract_file_name(self, response):
        """
        Get filename from response content-disposition
        """
        try:
            with response as r:
                fname = ""
                if "Content-Disposition" in r.headers.keys():
                    fname = re.findall(
                        "filename=(.+)", r.headers["Content-Disposition"]
                    )[0]
                else:
                    fname = r.url.split("?")[0].split("/")[-1]

                return fname.replace('"', "")
        except Exception:
            return "file.unknown"

    def hide(self, _=None):
        """Hides the modal overlay."""
        self.overlay.layout.display = "none"

    def show(self, response):
        """Displays the modal overlay."""
        self.overlay.layout.display = "flex"
        self.response = response

    def display(self):
        """Displays the modal in the notebook."""
        display(self.overlay)


class SpinnerWidget:
    def __init__(self):
        self.spinner_html = """
        <div id="spinner-container" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            display: none;
            justify-content: center;
            align-items: center;">
            <div class="spinner" style="
                border: 4px solid rgba(0, 0, 0, 0.1);
                border-top: 4px solid #3498db;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;"></div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        """

        self.spinner_out = widgets.Output()
        self.spinner_out.append_display_data(HTML(self.spinner_html))
    
    def show(self):
        """Show the spinner by injecting the HTML into the notebook body."""
        self.spinner_out.append_display_data(
            Javascript(
                """
                var spinner = document.getElementById('spinner-container');
                if (spinner) {
                    document.getElementById('spinner-container').style.display = 'flex';
                } else {
                    console.error('Spinner not found.');
                }
                """
            )
        )

    def hide(self):
        """Hide the spinner by changing the display style."""
        self.spinner_out.append_display_data(
            Javascript(
                """
                var spinner = document.getElementById('spinner-container');
                if (spinner) {
                    spinner.style.display = 'none';
                } else {
                    console.error('Spinner not found.');
                }
                """
            )
        )

    def display(self):
        """Display the spinner widget in the notebook."""
        display(self.spinner_out)
