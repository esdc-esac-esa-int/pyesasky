# pyesasky

Welcome to the ESASky Jupyter notebook widget page. 

# Requirements

Jupyter and node. Jupyter comes together with anaconda. 
To install node run the following command:

$ pip install npm

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

# Pyesaky in Jupyter lab

In order to be able to run pyesasky in Jupyter lab it is necessary to install the labextension ivywidgets by the following command:

$ jupyter labextension install @jupyter-widgets/jupyterlab-manager

NOTE that this requires node.js to be installed. 


# Uninstall

$ sh uninstall.sh

In case the uninstall is complaining about a missing 'rimraf' command, try that first and then rerun the uninstall procedure:

$ npm install webpack-dev-server rimraf webpack -g
