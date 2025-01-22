from jupyter_server import serverapp
from pyesasky.widgets import ESASkyWidget  # noqa


try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode:
    # https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings

    warnings.warn("Importing 'pyesasky' outside a proper installation.")
    __version__ = "dev"


def _load_jupyter_server_extension(serverapp: serverapp):
    """
    This function is called when the extension is loaded.
    """
    pass


def _jupyter_server_extension_paths():
    return [{"module": "pyesasky"}]


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": "pyesasky"}]
