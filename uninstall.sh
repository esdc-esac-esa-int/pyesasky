#!/bin/bash

echo "uninstalling current version"
pip uninstall pyesasky
python setup.py clean
npm run clean
jupyter nbextension uninstall pyesasky

