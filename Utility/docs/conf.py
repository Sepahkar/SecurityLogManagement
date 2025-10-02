# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.append(os.path.abspath('../APIManager/Portal'))
sys.path.append(os.path.abspath('../APIManager/EIT'))
sys.path.append(os.path.abspath('../APIManager/HR'))
sys.path.append(os.path.abspath('../DateTimeManager'))
#sys.path.insert(0, os.path.abspath('../*'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Utility'
copyright = '2022, Erfan Rezaee'
author = 'Erfan Rezaee'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'pydata_sphinx_theme'
# html_theme = 'furo'
html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
