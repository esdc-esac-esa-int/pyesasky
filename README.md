# pyesasky

ESASky Jupyter widget - some Jupyter Notebook sample files in jupyter_samples folder

- pyESASky-basic.ipynb
- pyESASky-astroquery.ipynb (integration and overlay of Gaia DR2 data)



# Installation

For a development installation (requires npm),

$ git clone https://github.com/fab77/pyesasky.git

$ cd pyesasky

$ npm install

$ python setup.py install

$ pip install .

$ jupyter nbextension install --py --sys-prefix pyesasky

$ jupyter nbextension enable --py --sys-prefix pyesasky


or simply run 


$ sh reinstall.sh




# Run pyesasky


Once installed open Jupyter notebook

$ jupyter notebook


from pyesasky.pyesasky import ESASkyWidget

esasky = ESASkyWidget()

esasky



## go to a target by name
esasky.goToTargetName('M51')

## go to RA and Dec
esasky.setGoToRADec('10 0 2', '+10 1 23')
esasky.setGoToRADec('45', '+81.7')

## set the FoV in decimal degrees
esasky.setFoV(1)

## use the Planck color palette for the current HiPS
esasky.setHiPSColorPalette('PLANCK')

## use the Native color palette for the current HiPS
esasky.setHiPSColorPalette('NATIVE')




# Uninstall

$ cd pyesasky

$ pip uninstall pyesasky

$ python setup.py clean

$ npm run clean

$ jupyter nbextension uninstall pyesasky

In case the uninstall will complain about a missing 'rimraf' command, try that first and then rerun the uninstall procedure:

$ npm install webpack-dev-server rimraf webpack -g
