# pyESASky

Welcome to the ESASky Jupyter widget page. 

# Requirements

`Jupyter` comes together with anaconda. 

# Installation

```bash
$ pip install pyesasky
```

# pyesasky in Jupyter lab

```bash
$ jupyter labextension install pyesasky
```
In some cases you might also have to run these 2 commands to enable PyESASky in Jupyter

```bash
$ jupyter nbextension install --py pyesasky --sys-prefix
$ jupyter nbextension enable --py pyeasky --sys-prefix
```
In order to be able to run pyesasky in Jupyter lab it is necessary to install the labextension ivywidgets by the following command:

```bash
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

NOTE that this requires `node.js` to be installed. 

If you use conda, you can get it with:

```bash
conda install -c conda-forge nodejs
```

If you use Homebrew on Mac OS X:
```bash
brew install node
```
You can also download `Node.js` from the Node.js website https://nodejs.org/ and install it directly.


# Running pyESASky samples:

Multiple sample notebooks of the functionality in pyESASky can be found in https://github.com/esdc-esac-esa-int/pyesasky/tree/master/samples

For the basic functionalities, open the pyESASky-Basic.ipynb. To check how to overlay a catalogue, run the pyESASky-Catalogue.ipynb. To overlay a set of footprints, open pyESASky-Footprints.ipynb .

# Run pyesasky

In general, it is possible to instantiate pyESASky by running the folowing code in your Jupyter Notebook.

```python
from pyesasky import ESASkyWidget
esasky = ESASkyWidget()
esasky
```
To be able to use catalogue features, the following additional classes must be imported:

```python
from pyesasky import Catalogue
from pyesasky import CatalogueDescriptor
from pyesasky import MetadataDescriptor
from pyesasky import MetadataType
```

To be able to use footprints features, the following additional classes must be imported:

```python
from pyesasky import FootprintSet
from pyesasky import FootprintSetDescriptor
from pyesasky import MetadataDescriptor
from pyesasky import MetadataType
```

# Source code installation

For a development installation (requires npm),
```bash
$ git clone https://github.com/esdc-esac-esa-int/pyesasky
$ cd pyesasky
$ sh install.sh
```
