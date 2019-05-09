# pyesasky

ESASky Jupyter widget - some Jupyter Notebook sample files in jupyter_samples folder

- pyESASky-basic.ipynb
- pyESASky-astroquery.ipynb (integration and overlay of Gaia DR2 data)



# Installation

For a development installation (requires npm),

$ git clone https://github.com/esdc-esac-esa-int/pyesasky

$ cd pyesasky

$ pip install .

$ jupyter nbextension install --py --sys-prefix pyesasky

$ jupyter nbextension enable --py --sys-prefix pyesasky


or simply run 

$ sh install.sh



# Run pyesasky


Running pyESASky samples:

$ cd samples

$ jupyter notebook

For the basic functionnalities, open the pyESASky-Basic.ipynb. To check how to overlay a catalogue, run the pyESASky-Catalogue.ipynb. To overlay a set of footprints, open pyESASky-Footprints.ipynb .

In general, it is possible to instantiate pyESASky by running the folowing code in your Jupyter Notebook.

from pyesasky.pyesasky import ESASkyWidget
esasky = ESASkyWidget()
esasky

To be able to use catalogue features, the following additional classes must be imported:

from pyesasky.pyesasky import Catalogue
from pyesasky.pyesasky import CatalogueDescriptor
from pyesasky.pyesasky import MetadataDescriptor
from pyesasky.pyesasky import MetadataType

To be able to use footprints features, the following additional classes must be imported:

from pyesasky.pyesasky import FootprintSet
from pyesasky.pyesasky import FootprintSetDescriptor
from pyesasky.pyesasky import MetadataDescriptor
from pyesasky.pyesasky import MetadataType




# Uninstall

$ pip uninstall pyesasky

$ jupyter nbextension uninstall pyesasky

In case the uninstall is complaining about a missing 'rimraf' command, try that first and then rerun the uninstall procedure:

$ npm install webpack-dev-server rimraf webpack -g
