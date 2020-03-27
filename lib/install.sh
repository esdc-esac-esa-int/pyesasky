#!/bin/bash
echo "installing pyesasky"
pip install .
jupyter nbextension install --py --sys-prefix pyesasky
jupyter nbextension enable --py --sys-prefix pyesasky
