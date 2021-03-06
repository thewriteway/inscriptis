==================================================================================
inscriptis -- HTML to text conversion library, command line client and Web service
==================================================================================

.. image:: https://img.shields.io/pypi/pyversions/inscriptis   
   :target: https://badge.fury.io/py/inscriptis
   :alt: Supported python versions

.. image:: https://api.codeclimate.com/v1/badges/f8ed73f8a764f2bc4eba/maintainability
   :target: https://codeclimate.com/github/weblyzard/inscriptis/maintainability
   :alt: Maintainability

.. image:: https://codecov.io/gh/weblyzard/inscriptis/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/weblyzard/inscriptis/
   :alt: Coverage

.. image:: https://github.com/weblyzard/inscriptis/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/weblyzard/inscriptis/actions/workflows/python-package.yml
   :alt: Build status

.. image:: https://readthedocs.org/projects/inscriptis/badge/?version=latest
   :target: https://inscriptis.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status

.. image:: https://badge.fury.io/py/inscriptis.svg
   :target: https://badge.fury.io/py/inscriptis
   :alt: PyPI version

.. image:: https://pepy.tech/badge/inscriptis
   :target: https://pepy.tech/project/inscriptis
   :alt: PyPI downloads

A python based HTML to text conversion library, command line client and Web
service with support for **nested tables**, a **subset of CSS** and optional
support for providing an **annotated output**.
Please take a look at the
`Rendering <https://github.com/weblyzard/inscriptis/blob/master/RENDERING.md>`_
document for a demonstration of inscriptis' conversion quality.

A Java port of inscriptis 1.x is available
`here <https://github.com/x28/inscriptis-java>`_.

This document provides a short introduction to Inscriptis. The full
documentation is built automatically and published on
`Read the Docs <https://inscriptis.readthedocs.org/en/latest/>`_.


.. contents:: Table of Contents


Installation
============

At the command line::

    $ pip install inscriptis

Or, if you don't have pip installed::

    $ easy_install inscriptis

If you want to install from the latest sources, you can do::

    $ git clone https://github.com/weblyzard/inscriptis.git
    $ cd inscriptis
    $ python setup.py install


Python library
==============

Embedding inscriptis into your code is easy, as outlined below:

.. code-block:: python
   
   import urllib.request
   from inscriptis import get_text
   
   url = "https://www.fhgr.ch"
   html = urllib.request.urlopen(url).read().decode('utf-8')
   
   text = get_text(html)
   print(text)


Standalone command line client
==============================
The command line client converts HTML files or text retrieved from Web pages to
the corresponding text representation.


Command line parameters
-----------------------
The inscript.py command line client supports the following parameters::

  usage: inscript.py [-h] [-o OUTPUT] [-e ENCODING] [-i] [-d] [-l] [-a] [-r ANNOTATION_RULES] [-p POSTPROCESSOR]
                     [--indentation INDENTATION] [-v]
                     [input]
  
  Convert the given HTML document to text.
  
  positional arguments:
    input                 Html input either from a file or a URL (default:stdin).
  
  optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                          Output file (default:stdout).
    -e ENCODING, --encoding ENCODING
                          Input encoding to use (default:utf-8 for files; detected server encoding for Web URLs).
    -i, --display-image-captions
                          Display image captions (default:false).
    -d, --deduplicate-image-captions
                          Deduplicate image captions (default:false).
    -l, --display-link-targets
                          Display link targets (default:false).
    -a, --display-anchor-urls
                          Deduplicate image captions (default:false).
    -r ANNOTATION_RULES, --annotation-rules ANNOTATION_RULES
                          Path to an optional JSON file containing rules for annotating the retrieved text.
    -p POSTPROCESSOR, --postprocessor POSTPROCESSOR
                          Optional component for postprocessing the result (html, surface, xml).
    --indentation INDENTATION
                          How to handle indentation (extended or strict; default: extended).
    -v, --version         display version information
   

Examples
--------

HTML to text conversion
~~~~~~~~~~~~~~~~~~~~~~~
convert the given page to text and output the result to the screen::

  $ inscript.py https://www.fhgr.ch
   
convert the file to text and save the output to output.txt::

  $ inscript.py fhgr.html -o fhgr.txt
   
convert HTML provided via stdin and save the output to output.txt::

  $ echo '<body><p>Make it so!</p>></body>' | inscript.py -o output.txt 


HTML to annotated text conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
convert and annotate HTML from a Web page using the provided annotation rules::

  $ inscript.py https://www.fhgr.ch -r ./examples/annotation-profile.json

The annotation rules are specified in `annotation-profile.json`:

.. code-block:: json

   {
    "h1": ["heading", "h1"],
    "h2": ["heading", "h2"],
    "b": ["emphasis"],
    "div#class=toc": ["table-of-contents"],
    "#class=FactBox": ["fact-box"],
    "#cite": ["citation"]
   }

The dictionary maps an HTML tag and/or attribute to the annotations
inscriptis should provide for them. In the example above, for instance, the tag
`h1` yields the annotations `heading` and `h1`, a `div` tag with a
`class` that contains the value `toc` results in the annotation
`table-of-contents`, and all tags with a `cite` attribute are annotated with
`citation`.

Given these annotation rules the HTML file

.. code-block:: HTML

   <h1>Chur</h1>
   <b>Chur</b> is the capital and largest town of the Swiss canton of the
   Grisons and lies in the Grisonian Rhine Valley.

yields the following JSONL output

.. code-block:: json

   {"text": "Chur\n\nChur is the capital and largest town of the Swiss canton
             of the Grisons and lies in the Grisonian Rhine Valley.",
    "label": [[0, 4, "heading"], [0, 4, "h1"], [6, 10, "emphasis"]]}

The provided list of labels contains all annotated text elements with their
start index, end index and the assigned label.

Annotation postprocessors
~~~~~~~~~~~~~~~~~~~~~~~~~
Annotation postprocessors enable the post processing of annotations to formats
that are suitable for you particular application. Post processors can be
specified with the `-p` or `--postprocessor` command line argument::

  $ inscript.py https://www.fhgr.ch \
          -r ./examples/annotation-profile.json \
          -p tag


Output:

.. code-block:: json

   {"text": "  Chur\n\n  Chur is the capital and largest town of the Swiss
             canton of the Grisons and lies in the Grisonian Rhine Valley.",
    "label": [[0, 6, "heading"], [8, 14, "emphasis"]],
    "tag": "<heading>Chur</heading>\n\n<emphasis>Chur</emphasis> is the
           capital and largest town of the Swiss canton of the Grisons and
           lies in the Grisonian Rhine Valley."}



Currently, inscriptis supports the following postprocessors:

- surface: returns a list of mapping between the annotation's surface form and its label::

    [
       ['heading', 'Chur'], 
       ['emphasis': 'Chur']
    ]

- xml: returns an additional annotated text version::

    <?xml version="1.0" encoding="UTF-8" ?>
    <heading>Chur</heading>

    <emphasis>Chur</emphasis> is the capital and largest town of the Swiss
    canton of the Grisons and lies in the Grisonian Rhine Valley.

- html: creates an HTML file which contains the converted text and highlights all annotations as outlined below:

.. figure:: https://github.com/weblyzard/inscriptis/raw/master/docs/paper/images/annotations.png
   :align: left
   :alt: Annotations extracted from the Wikipedia entry for Chur wht the `--postprocess html` postprocessor.

   Snippet of the rendered HTML file created with the following command line options and annotation rules:

   .. code-block:: bash

      inscript.py --annotation-rules ./wikipedia.json \
                  --postprocessor html \
                  https://en.wikipedia.org/wiki/Chur.html

   Annotation rules encoded in the `wikipedia.json` file:

   .. code-block:: json

      {
        "h1": ["heading"],
        "h2": ["heading"],
        "h3": ["subheading"],
        "h4": ["subheading"],
        "h5": ["subheading"],
        "i": ["emphasis"],
        "b": ["bold"],
        "table": ["table"],
        "th": ["tableheading"],
        "a": ["link"]
      } 


Web Service
===========

The Flask Web Service translates HTML pages to the corresponding plain text.

Additional Requirements
-----------------------

* python3-flask

Startup
-------
Start the inscriptis Web service with the following command::

  $ export FLASK_APP="web-service.py"
  $ python3 -m flask run

Usage
-----

The Web services receives the HTML file in the request body and returns the
corresponding text. The file's encoding needs to be specified
in the `Content-Type` header (`UTF-8` in the example below)::

  $ curl -X POST  -H "Content-Type: text/html; encoding=UTF8"  \
          --data-binary @test.html  http://localhost:5000/get_text

The service also supports a version call::

  $ curl http://localhost:5000/version


Advanced topics
===============

Annotated text
--------------
Inscriptis can provide annotations alongside the extracted text which allows
downstream components to draw upon semantics that have only been available in
the original HTML file.

The extracted text and annotations can be exported in different formats,
including the popular JSONL format which is used by
`doccano <https://github.com/doccano/doccano>`_.

Example output:

.. code-block:: json

   {"text": "Chur\n\nChur is the capital and largest town of the Swiss canton
             of the Grisons and lies in the Grisonian Rhine Valley.",
    "label": [[0, 4, "heading"], [0, 4, "h1"], [6, 10, "emphasis"]]}

The output above is produced, if inscriptis is run with the following
annotation rules:

.. code-block:: json

   {
    "h1": ["heading", "h1"],
    "b": ["emphasis"],
   }

The code below demonstrates how inscriptis' annotation capabilities can
be used within a program:

.. code-block:: python

  import urllib.request
  from inscriptis import get_annotated_text, ParserConfig

  url = "https://www.fhgr.ch"
  html = urllib.request.urlopen(url).read().decode('utf-8')

  rules = {'h1': ['heading', 'h1'],
           'h2': ['heading', 'h2'],
           'b': ['emphasis'],
           'table': ['table']
          }

  output = get_annotated_text(html, ParserConfig(annotation_rules=rules)
  print("Text:", output['text'])
  print("Annotations:", output['label'])

Fine tuning
-----------

The following options are available for fine tuning inscriptis' HTML rendering:

1. **More rigorous indentation:** call `inscriptis.get_text()` with the
   parameter `indentation='extended'` to also use indentation for tags such as
   `<div>` and `<span>` that do not provide indentation in their standard
   definition. This strategy is the default in `inscript.py` and many other
   tools such as lynx. If you do not want extended indentation you can use the
   parameter `indentation='standard'` instead.

2. **Overwriting the default CSS definition:** inscriptis uses CSS definitions
   that are maintained in `inscriptis.css.CSS` for rendering HTML tags. You can
   override these definitions (and therefore change the rendering) as outlined
   below:

.. code-block:: python

      from lxml.html import fromstring
      from inscriptis.css_profiles import CSS_PROFILES, HtmlElement
      from inscriptis.html_properties import Display
      from inscriptis.model.config import ParserConfig
      
      # create a custom CSS based on the default style sheet and change the
      # rendering of `div` and `span` elements
      css = CSS_PROFILES['strict'].copy()
      css['div'] = HtmlElement(display=Display.block, padding=2)
      css['span'] = HtmlElement(prefix=' ', suffix=' ')
      
      html_tree = fromstring(html)
      # create a parser using a custom css
      config = ParserConfig(css=css)
      parser = Inscriptis(html_tree, config)
      text = parser.get_text()
   

Changelog
=========

A full list of changes can be found in the
`release notes <https://github.com/weblyzard/inscriptis/releases>`_.
