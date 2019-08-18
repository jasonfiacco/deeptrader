# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import subprocess
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------

project = 'TensorTrade'
copyright = '2019, Adam King'
author = 'Adam King'

# Read version
exec(open('../../tensortrade/version.py').read())
# short X.Y version
version = __version__
# The full version, including alpha/beta/rc tags
release = __version__

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinxcontrib.apidoc',  # automatically generate API docs, see https://github.com/rtfd/readthedocs.org/issues/1139
    'nbsphinx',
    'nbsphinx_link',  # for linking notebooks from outside sphinx source root
    'm2r'
]

# nbsphinx settings
nbsphinx_execute = 'auto'

# apidoc settings
apidoc_module_dir = '../../tensortrade'
apidoc_output_dir = 'api'
apidoc_excluded_paths = ['**/*test*']
apidoc_module_first = True
apidoc_separate_modules = True
apidoc_extra_args = ['-d 6']

# mock imports
autodoc_mock_imports = ['tensorflow', 'keras', 'sklearn']

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']
# source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['build', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# https://sphinx-rtd-theme.readthedocs.io/en/latest/configuring.html
html_theme_options = {
    'logo_only': True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# override default theme width
html_context = {
    'css_files': [
        '_static/theme_overrides.css',  # override wide tables in RTD theme
    ],
}

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'tensortradedocs'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'tensortrade.tex', 'tensortrade Documentation',
     'Adam King', 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'tensortrade', 'tensortrade Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'tensortrade', 'tensortrade Documentation',
     author, 'tensortrade', 'An open source reinforcement learning framework for training, evaluating, and deploying robust trading agents.',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# from https://github.com/vidartf/nbsphinx-link/blob/master/docs/source/conf.py

# Ensure env.metadata[env.docname]['nbsphinx-link-target']
# points relative to repo root:
here = os.path.dirname(__file__)
repo = os.path.join(here, '..', '..')
nbsphinx_link_target_root = repo

# from https://github.com/vidartf/nbsphinx-link/blob/master/docs/source/conf.py for custom tags
try:
    git_rev = subprocess.check_output(
        ['git', 'describe', '--exact-match', 'HEAD'], universal_newlines=True)
except subprocess.CalledProcessError:
    try:
        git_rev = subprocess.check_output(['git', 'rev-parse', 'HEAD'], universal_newlines=True)
    except subprocess.CalledProcessError:
        git_rev = ''
if git_rev:
    git_rev = git_rev.splitlines()[0] + '/'

nbsphinx_prolog = (
    r"""
{% if env.metadata[env.docname]['nbsphinx-link-target'] %}
{% set docpath = env.metadata[env.docname]['nbsphinx-link-target'] %}
{% else %}
{% set docpath = env.doc2path(env.docname, base='docs/source/') %}
{% endif %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html
    
    .. nbinfo::
        This page was generated from `{{ docpath }}`__.
    
    __ https://github.com/notadamking/tensortrade/blob/
        """ +
    git_rev + r"{{ docpath }}"
)
