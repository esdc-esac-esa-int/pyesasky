from ._version import version_info, __version__ # noqa
from .pyesasky import ESASkyWidget # noqa
from .catalogue import Catalogue # noqa
from .catalogueDescriptor import CatalogueDescriptor # noqa
from .cooFrame import CooFrame # noqa
from .footprintSet import FootprintSet # noqa
from .footprintSetDescriptor import FootprintSetDescriptor # noqa
from .HiPS import HiPS # noqa
from .imgFormat import ImgFormat # noqa
from .jupyter_server import load_jupyter_server_extension # noqa
from .metadataDescriptor import MetadataDescriptor # noqa
from .metadataType import MetadataType # noqa


# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [{'section': 'notebook',
            # the path is relative to the `pyesasky` directory
            'src': 'nbextension/static',
            # directory in the `nbextension/` namespace
            'dest': 'pyesasky',
            # _also_ in the `nbextension/` namespace
            'require': 'pyesasky/extension'}]


def _jupyter_server_extension_paths():
    return [{"module": "pyesasky"}]