# pyesasky

Welcome to the ESASky Jupyter notebook widget page. 


# Installation

For a development installation (requires npm),

$ git clone https://github.com/esdc-esac-esa-int/pyesasky

$ cd pyesasky

$ sh install.sh


# Running pyESASky samples:

$ cd samples

$ jupyter notebook

For the basic functionnalities, open the pyESASky-Basic.ipynb. To check how to overlay a catalogue, run the pyESASky-Catalogue.ipynb. To overlay a set of footprints, open pyESASky-Footprints.ipynb .


# Run pyesasky

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

$ sh uninstall.sh

In case the uninstall is complaining about a missing 'rimraf' command, try that first and then rerun the uninstall procedure:

$ npm install webpack-dev-server rimraf webpack -g
