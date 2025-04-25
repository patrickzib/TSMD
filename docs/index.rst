.. TSMD documentation master file, created by
   sphinx-quickstart
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TSMD's documentation!
===================================

.. toctree::
   :maxdepth: 1
   :hidden:

   overview/index
   algorithms/index
   datasets/index
   evaluation/index
   guidelines/index


Overview
--------

The TSMD project brings together Motif Discovery methods for Time Series, aiming to compare their performance through well-defined research questions and to simplify their practical use. It provides both guidelines for selecting the most suitable methods based on the data, and accessible implementations of the most relevant approaches.

Installation
^^^^^^^^^^^^

Install tsmd with pip
~~~~~~~~~~~~~~~~~~~~~
You can install tsmd using pip: 

.. code-block:: bash

   pip install tsmd
Install tsmd from source 
~~~~~~~~~~~~~~~~~~~~~~~~

The following tools are required to install TSMD from source:

- git
- conda (anaconda or miniconda)


Clone this `repository <https://github.com/grrvlr/TSMD.git>`_ using git and go into its root directory.

.. code-block:: bash

   git clone https://github.com/grrvlr/TSMD.git
   cd TSMD/

Create and activate a conda-environment 'TSMD'.

.. code-block:: bash

   conda env create --file environment.yml
   conda activate TSMD

Usage
^^^^^

We depicts below a code snippet demonstrating how to use one motif detection algorithm (in this example, we first generate a synthetic time series).

.. code-block:: python

   from data.Synthetic.synthetic_signal import SignalGenerator

   generator=SignalGenerator(n_motifs=2, motif_length=200, motif_amplitude=3, motif_fundamental=3, sparsity=0.5, sparsity_fluctuation=0.5)
   signal,labels= generator.generate()
   generator.plot()
   
.. image:: ../assets/methodExample/signal_example.png
   :alt: Synthetic signal
   :align: center
   :target: ../assets/methodExample/signal_example.png

.. code-block:: python 

   from tsmd.competitors.persistence import BasePersistentPattern
   from tsmd.tools.utils import transform_label
   from tsmd.tools.plotting import plot_signal_pattern


   pepa=BasePersistentPattern(wlen_for_persistence=180, n_patterns=2)
   pepa.fit(signal)

.. image:: /../assets/methodExample/pepa_example.png
   :alt: PEPA output
   :align: center

labels=transform_label(pepa.prediction_mask_)
plot_signal_pattern(signal,labels)


License
^^^^^^^

The project is licensed under the `MIT license <https://mit-license.org>`_.

If you use TSMD in your project or research, please cite the following paper:

   Time Series Motif Discovery: A Comprehensive Evaluation
   Valerio Guerrini, Thibaut Germain, Charles Truong, Laurent Oudre, Paul Boniol.
   Proceedings of the VLDB Endowment (PVLDB 2025) Journal, Volume 18.

You can use the following BibTeX entries:

.. code-block:: bibtex

   @article{Guerrini2025tsmd,
      title={Time Series Motif Discovery: A Comprehensive Evaluation},
      author={Guerrini, Valerio and Germain, Thibaut and Truong, Charles and Oudre, Laurent and Boniol, Paul},
      journal={Proceedings of the VLDB Endowment},
      volume={18},
      number={7},
      year={2025},
      publisher={VLDB Endowment}
   }

Contributors
^^^^^^^^^^^^

- Valerio Guerrini (Centre Borelli, ENS Paris Saclay, Université Paris Cité)
- Thibaut Germain (Centre Borelli, ENS Paris Saclay, Université Paris Cité)
- Charles Truong (Centre Borelli, ENS Paris Saclay, Université Paris Cité)
- Laurent Oudre (Centre Borelli, ENS Paris Saclay, Université Paris Cité)
- Paul Boniol (Inria, ENS, CNRS, PLS University)
