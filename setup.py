"""
pyesasky setup
"""
import json
from pathlib import Path
from os.path import join as pjoin 

from jupyter_packaging import (
    wrap_installers,
    npm_builder,
    get_data_files,
    install_npm
)
import setuptools

HERE = Path(__file__).parent.resolve()

# The name of the project
name = "pyesasky"

lab_path = (HERE / name / "labextension")
nb_path = (HERE /name / 'nbextension')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    pjoin(HERE, 'lib', 'plugin.js'),
    pjoin(HERE, 'lib', 'extension.js'),
]

# Representative files that should exist after a successful build
ensured_targets = [
    str(lab_path / "package.json"),
    str(lab_path / "static/style.js"),
    pjoin(nb_path, 'index.js'),
    pjoin(HERE, 'lib', 'plugin.js'),
    pjoin(HERE, 'lib', 'extension.js'),
]

labext_name = "pyesasky"
package_data_spec = {
    'pyesasky': [
        'nbextension/static/*.*js*'
    ]
}
data_files_spec = [
    ("share/jupyter/nbextensions/pyesasky", str(nb_path), "**"),
    ("share/jupyter/labextensions/pyesasky", str(lab_path), "**"),
    ("share/jupyter/labextensions/pyesasky", str(HERE), "install.json"),
    ('etc/jupyter/nbconfig/notebook.d' , pjoin(HERE, 'jupyter.d', 'notebook.d'), 'pyesasky.json'),
    ('etc/jupyter/jupyter_notebook_config.d' , pjoin(HERE, 'jupyter.d', 'jupyter_notebook_config.d'), 'pyesasky.json'),
]

post_develop = npm_builder(
    build_cmd="install:extension", source_dir="src", build_dir=lab_path
)

# pre_develop = install_npm(HERE, npm=["yarn"], build_cmd='build:extensions')

cmdclass = wrap_installers(post_develop=post_develop, ensured_targets=ensured_targets)

long_description = (HERE / "README.md").read_text()

# Get the package info from package.json
pkg_json = json.loads((HERE / "package.json").read_bytes())

setup_args = dict(
    name=name,
    version=pkg_json["version"],
    url=pkg_json["homepage"],
    author=pkg_json["author"]["name"],
    author_email=pkg_json["author"]["email"],
    description=pkg_json["description"],
    license=pkg_json["license"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    cmdclass=cmdclass,
    data_files=get_data_files(data_files_spec),
    packages=setuptools.find_packages(),
    install_requires=[
        'ipywidgets>=7.6.3',
        'ipykernel>=5.0.0',
        'requests>=2.5.1'
    ],
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab", "JupyterLab3"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
