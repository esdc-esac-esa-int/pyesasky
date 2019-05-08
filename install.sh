#!/bin/bash
echo "installing"
npm install
npm i @jupyterlab/coreutils
python setup.py install
pip install .
jupyter nbextension install --py --sys-prefix pyesasky
jupyter nbextension enable --py --sys-prefix pyesasky
