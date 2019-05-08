#!/bin/bash




# uninstall
echo "uninstalling current version"
pip uninstall pyesasky
jupyter nbextension uninstall pyesasky

sleep 2

# install
echo "installing pyesaky"
pip install .
jupyter nbextension install --py --sys-prefix pyesasky
jupyter nbextension enable --py --sys-prefix pyesasky
