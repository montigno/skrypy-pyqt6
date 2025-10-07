.. Skrypy Documentation documentation master file, created by
   sphinx-quickstart on Mon Jul 28 14:43:46 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Skrypy documentation! 
==================================== 

(documentation still in development)
------------------------------------

Skrypy offers a graphical programming approach that helps you visualize every aspect of your application and pipeline.

In particular, it allows you to:

- program your logic or pipeline using intuitive graphical programming (diagram editor)
- manage and visualize your data (images, spectra, etc.)
- interact with other software tools (Deep learning, Nipype, MRTrix, ANTs, FSL, Matlab engine and others of your choice)
- manage environment variables (without touching your OS configuration file such as .bashrc)
- execute routine tasks
- execute several different pipelines (shared memory tools allow parameters to be exchanged, even between client-cluster)
- execute your pipelines locally or on a cluster (HPC), for deep learning for example

It is developed in Python and uses the PyQt5 framework. |br|
Its installation is done in a virtual environment (virtualenv).

.. image:: ./ressources/Skrypy_interface.png
   :width: 800
   :alt: (skrypy interface)

Features
========

Skrypy is primarily intended for processing MRI images:

- importation (Dicom, Nifti, Bruker, Philips Achieva and others)
- visualization (2D to 5D with ImageJ, FSLeyes, mrview and others)
- registration
- segmentation, skullstripping
- diffusion, tractography
- analyze (Bvf, Cbf, T1map, T2map, ...)
- filtering (N4bias, smoothing, unifize ...)
- and many more!

But it can also be used for other purposes:

- to test codes and functions
- to do simulation
- to execute routine tasks (file transfer via SCP, memory cleaning, rename files in bulk, etc...)
- and many more! 

Specifically, Skrypy features:

- a rich library of calculation blocks (you can add/create your own block very easily)
- an 'For' loop structure (which can be executed sequentially or in multithreading/multiprocessing mode)
- an 'If' structure
- a 'script' structure that allows you to combine textual programming in Python with graphical programming (this allows you to fill in the missing tools in the blocks library)
- graphic elements (spinbox, textedit, combobox, etc...) which allow you to create constants visually and easily

.. image:: ./ressources/Skrypy_items.png
   :width: 800
   :alt: (skrypy items)


Table of Contents
==================

.. toctree::
   :maxdepth: 1
   :caption: Install

   installation/requirements.rst
   installation/install_skrypy.rst
   installation/package_install.rst
   installation/install_dependencies.rst
   installation/cluster.rst
   installation/update_skrypy.rst

.. toctree::
   :maxdepth: 1
   :caption: Getting started

   start/running_skrypy.rst
   start/demo_1.rst
   start/shared_memory.rst

.. toctree::
   :maxdepth: 1
   :caption: Blocks

   blocks/create_blocks.rst

.. toctree::
   :maxdepth: 1
   :caption: Reference

   reference/preinstalled_packages_list.rst

.. toctree::
   :maxdepth: 1
   :caption: Troubleshooting

   troubleshooting/trblsh.rst

.. # define a hard line break for HTML
.. |br| raw:: html

   <br />
