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
import os
import sys
from neorl.version import version
# We CANNOT enable 'sphinxcontrib.spelling' because ReadTheDocs.org does not support
# PyEnchant.
try:
    import sphinxcontrib.spelling
    enable_spell_check = True
except ImportError:
    enable_spell_check = False

# source code directory, relative to this file, for sphinx-autobuild
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../neorl'))

#class Mock(MagicMock):
#    @classmethod
#    def __getattr__(cls, name):
#        return MagicMock()

# Mock modules that requires C modules
# Note: because of that we cannot test examples using CI
#MOCK_MODULES = ['joblib', 'scipy', 'scipy.signal',
#                'mpi4py', 'mujoco-py', 'cv2', 'tensorflow',
#                'tensorflow.contrib', 'tensorflow.contrib.layers',
#                'tensorflow.python', 'tensorflow.python.client', 'tensorflow.python.ops',
#                'tqdm', 'matplotlib', 'matplotlib.pyplot',
#                'seaborn', 'tensorflow.core', 'tensorflow.core.util', 'tensorflow.python.util',
#                'zmq']
#sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# Read version from file
#version_file = os.path.join(os.path.dirname(__file__), '../../../neorl', 'version.txt')
version_file =  '../../neorl/version.txt'
__version__ = version()

# -- Project information -----------------------------------------------------

project = 'NEORL'
copyright = '2021, Exelon Corp. & MIT'
author = 'Majdi I. Radaideh and NEORL Team'

# The short X.Y version
version = 'main (' + __version__ + ' )'
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
    'sphinx.ext.autosummary',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
]

if enable_spell_check:
    extensions.append('sphinxcontrib.spelling')

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

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
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# Fix for read the docs
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    html_theme = 'default'
else:
    html_theme = 'sphinx_rtd_theme'

html_logo = '_static/img/logo.png'


def setup(app):
    #app.add_stylesheet("css/baselines_theme.css")
    app.add_stylesheet("css/theme_overrides.css")

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

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
htmlhelp_basename = 'neorldoc'


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
    (master_doc, 'neorl.tex', 'NEORL Documentation',
     'NEORL Contributors', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'neorl', 'NEORL Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'NEORL', 'NEORL Documentation',
     author, 'NEORL', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------
