NURBS-Python
^^^^^^^^^^^^

|DOI|_ |RTFD|_ |WAFFLEIO|_

Introduction
============

This project aims to implement Non-Uniform Rational B-Spline (NURBS) curve and surface computation algorithms in native
Python with minimum possible dependencies. The library is fully object-oriented and does *not* depend on any external
C/C++ libraries.

The package contains 3 modules:

* :code:`BSpline` contains Non-Uniform B-Spline (NUBS) evaluation and storage functionality
* :code:`NURBS` contains Non-Uniform Rational B-Spline (NURBS) evaluation and storage functionality
* :code:`CPGen` contains simple control points grid generation algorithms

:code:`BSpline` and :code:`NURBS` modules contain 3 classes for geometric evaluation:

* **Curve** for evaluating 3D curves
* **Curve2D** for evaluating 2D curves
* **Surface** for evaluating surfaces

:code:`CPGen` module contains 2 classes for grid generation:

* **Grid** for generating inputs for :code:`BSpline.Surface` class
* **GridWeighted** for generating inputs for :code:`NURBS.Surface` class

Information for Researchers
---------------------------

I would be glad if you cite this repository using the DOI_ provided as a badge at the top.

Library Versions
----------------

* ``master`` branch contains the latest version of NURBS-Python (currently v3.x series).
* ``2.x`` branch contains the code for *NURBS-Python v2.x* series.

There are some API changes between *v2.x* and *v3.x* series and all updates will be added to the latest version. Old
versions won't be receiving any new features and updates.

Installation
============

Included *setup.py* script will take care of the installation and automatically copy the required files to
*site-packages* directory. Please run the following from the command line:

``python setup.py install``

If you don't want to put the files into your Python distribution's *site-packages* directory for some reason,
you can run

``python setup.py develop``

from the command line to generate a link to the package directory inside *site-packages*.

Example Scripts
===============

Please see `NURBS-Python Examples <https://github.com/orbingol/NURBS-Python_Examples>`_ repository for examples.

Implementation
==============

NURBS-Python is a high-level Python library following the object-oriented design principles. In its core, it implements
the algorithms from **The NURBS Book (2nd Edition)** by Piegl & Tiller and combines these algorithms with other useful
features. Please see the documentation for function reference and how to use the library: http://nurbs-python.rtfd.org

Issues and Reporting
====================

Bugs and Issues
---------------

Please use the issue tracker for reporting bugs and other related issues.

Comments and Questions
----------------------

If you have any questions or comments related to the NURBS-Python package, please don't hesitate to contact the
developers by email.

Author
======

* Onur Rauf Bingol (`@orbingol <https://github.com/orbingol>`_)

Contributors
============

I would like to thank all contributors for their help and support in testing, bug fixing and improvement of the
NURBS-Python_ project.

* Luke Frisken (`@kellpossible <https://github.com/kellpossible>`_)
* John-Eric Dufour (`@jedufour <https://github.com/jedufour>`_)
* Jan Heczko (`@heczis <https://github.com/heczis>`_)

License
=======

NURBS-Python is licensed under `The MIT License <LICENSE>`_.

Acknowledgments
===============

I would like to thank my PhD adviser, `Dr. Adarsh Krishnamurthy <https://www.me.iastate.edu/faculty/?user_page=adarsh>`_,
for his guidance and supervision throughout the course of this project.


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |RTFD| image:: https://readthedocs.org/projects/nurbs-python/badge/?version=latest
.. _RTFD: http://nurbs-python.readthedocs.io/en/latest/?badge=latest

.. |WAFFLEIO| image:: https://badge.waffle.io/orbingol/NURBS-Python.svg?columns=all
.. _WAFFLEIO: https://waffle.io/orbingol/NURBS-Python

.. _NURBS-Python: https://github.com/orbingol/NURBS-Python
