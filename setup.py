from __future__ import print_function

import os
from glob import glob
from os.path import join as pjoin 

from setupbase import (
    create_cmdclass, install_npm, ensure_targets,
    find_packages,  combine_commands, ensure_python, 
    get_version, HERE
)

from setuptools import setup

name = 'pyesasky'

# Ensure a valid python version
ensure_python('>=2.7')

# Get our version
version = get_version(pjoin(name, '_version.py'))

nb_path = pjoin(HERE, name, 'nbextension', 'static')
lab_path = pjoin(HERE, name, 'labextension') 

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    pjoin(HERE, 'lib', 'plugin.js'),
    pjoin(HERE, 'lib', 'extension.js'),
]

package_data_spec = {
    'pyesasky': [
        'nbextension/static/*.*js*',
        'nbextension/static/*.html',
        'labextension/*.tgz'
    ]
}

data_files_spec = [
    ('etc/jupyter/nbconfig/notebook.d' , os.path.join(HERE, 'jupyter.d', 'notebook.d'), 'pyesaky.json'),
    ('etc/jupyter/jupyter_notebook_config.d' , os.path.join(HERE, 'jupyter.d', 'jupyter_notebook_config.d'), 'pyesaky.json')]


cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
    data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(HERE, build_cmd='build:all'),
    ensure_targets(jstargets),
)


with open("README.md", "r") as fh:
    long_description = fh.read()


setup_args = dict(
    name                    = name,
    description             = 'ESASky Python wrapper',
    version                 = version,  
    scripts                 = glob(pjoin('scripts', '*')),
    cmdclass                = cmdclass,
    long_description        = long_description,
    long_description_content_type = "text/markdown",  
    packages                = find_packages(),
    author                  = 'Fabrizio Giordano <fgiordano@sciops.esa.int>, Mattias Wångblad <mattias@winterway.eu>, ESDC ', 
    #author_email            = 'fgiordano@sciops.esa.int',
    url                     = 'https://github.com/esdc-esac-esa-int/pyesasky',
    license                 = 'GNU Lesser General Public License',
    platforms               = 'Linux, Mac OS X, Windows',
    keywords                = ['ipython','jupyter','widgets'],
    classifiers             = [
        'Development Status :: 5 - Production/Stable',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    include_package_data    = True,
    data_files=[
        # like `jupyter nbextension install --sys-prefix`
        ("share/jupyter/nbextensions/pyesasky", [
            "pyesasky/nbextension/static/index.js",
        ]),
        # like `jupyter nbextension enable --sys-prefix`
        ("etc/jupyter/nbconfig/notebook.d", [
            "jupyter.d/jupyter_notebook_config.d/pyesasky.json"
        ]),
    ],
    install_requires        = [
        'numpy>=1.9',
        'matplotlib>1.5',
        'astropy>=1.0',
        'requests',
        'beautifulsoup4',
        'python-dateutil',
        'lxml',
        'ipywidgets>=7.5.1',
        'ipykernel>=5.0.0',
        'ipyevents',
        'traitlets',
        'qtpy',
        'flask',
        'flask-cors',
        'six',
        'requests',
        'configparser'
    ],    
    extras_require = {
        'test': [
            'pytest',
            'pytest-cov',
            'nbval',
        ],
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
            'sphinx>=1.5',
            'recommonmark',
            'sphinx_rtd_theme',
            'nbsphinx>=0.2.13',
            'jupyter_sphinx',
            'nbsphinx-link',
            'pytest_check_links',
            'pypandoc',
        ],
    },
    entry_points = {
    },
    zip_safe=False
)

if __name__ == '__main__':
    setup(**setup_args)
