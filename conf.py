# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Redmine Study Notes'
author = '9506hqwy'
copyright = '2022, 9506hqwy'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinxcontrib.mermaid',
]

exclude_patterns = [
    '.mypy_cache',
    '.venv',
    '.vscode',
    '_build',
]

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_style = 'css/styles.css'

# -- MyST configuration-------------------------------------------------------

myst_fence_as_directive = ["mermaid"]
myst_number_code_blocks = ["sh"]
