# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute.

# -- Project information -----------------------------------------------------
import os
import re
import sys
import time

import sphinx_gallery.gen_rst
from furo.gen_tutorials import generate_tutorials


# Path setup for building from source tree
sys.path.insert(0, os.path.abspath("."))  # For building from root
sys.path.insert(0, os.path.abspath(".."))  # For building from docs dir

import gymnasium  # noqa: E402


project = "Gymnasium"
copyright = f"{time.localtime().tm_year} Farama Foundation"
author = "Farama Foundation"

# The full version, including alpha/beta/rc tags
release = gymnasium.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
    "myst_parser",
    "furo.gen_tutorials",
    "sphinx_gallery.gen_gallery",
    "sphinx_github_changelog",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["tutorials/README.rst"]

# Napoleon settings
napoleon_use_ivar = True
napoleon_use_admonition_for_references = True
# See https://github.com/sphinx-doc/sphinx/issues/9119
napoleon_custom_sections = [("Returns", "params_style")]

# Autodoc
autoclass_content = "both"
autodoc_preserve_defaults = True


# This function removes the content before the parameters in the __init__ function.
# This content is often not useful for the website documentation as it replicates
# the class docstring.
def remove_lines_before_parameters(app, what, name, obj, options, lines):
    if what == "class":
        # ":param" represents args values
        first_idx_to_keep = next(
            (i for i, line in enumerate(lines) if line.startswith(":param")), 0
        )
        lines[:] = lines[first_idx_to_keep:]


def setup(app):
    app.connect("autodoc-process-docstring", remove_lines_before_parameters)


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"
html_title = "Gymnasium Documentation"
html_baseurl = "https://gymnasium.farama.org"
html_copy_source = False
html_favicon = "_static/img/favicon.png"
html_theme_options = {
    "light_logo": "img/gymnasium_black.svg",
    "dark_logo": "img/gymnasium_white.svg",
    "gtag": "G-6H9C8TWXZ8",
    "description": "A standard API for reinforcement learning and a diverse set of reference environments (formerly Gym)",
    "image": "img/gymnasium-github.png",
    "versioning": True,
    "source_repository": "https://github.com/Farama-Foundation/Gymnasium/",
    "source_branch": "main",
    "source_directory": "docs/",
}

html_static_path = ["_static"]
html_css_files = []

# -- Generate Tutorials -------------------------------------------------

sphinx_gallery.gen_rst.EXAMPLE_HEADER = """
.. DO NOT EDIT.
.. THIS FILE WAS AUTOMATICALLY GENERATED BY SPHINX-GALLERY.
.. TO MAKE CHANGES, EDIT THE SOURCE PYTHON FILE:
.. "{0}"
.. LINE NUMBERS ARE GIVEN BELOW.

.. rst-class:: sphx-glr-example-title

.. _sphx_glr_{1}:

"""

sphinx_gallery_conf = {
    "ignore_pattern": r"__init__\.py",
    "examples_dirs": "./tutorials",
    "gallery_dirs": "./tutorials",
    "copyfile_regex": r"./tutorials/.*\.md",
    "show_signature": False,
    "show_memory": False,
    "min_reported_time": float("inf"),
    "filename_pattern": f"{re.escape(os.sep)}run_",
    "default_thumb_file": os.path.join(
        os.path.dirname(__file__), "_static/img/gymnasium-github.png"
    ),
}

# All tutorials in the tutorials directory will be generated automatically
# by sphinx-gallery.
# However, we also want to generate some tutorials without the gallery
# and to a more specific location so we use this custom function.
generate_tutorials("introduction/*.py", "./introduction")

# -- Generate Changelog -------------------------------------------------

sphinx_github_changelog_token = os.environ.get("SPHINX_GITHUB_CHANGELOG_TOKEN")