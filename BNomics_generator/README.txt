
This README describes a collection of python scripts for the Bayes Network (BN)
structure learning problem collectively called BNOmics. The software allows for
a purely data driven BN structure learning and is best used in combination with
a python shell, such as Ipython, for on-the-fly experimentation and research.
It could, however, be easily used for stand alone scripts such as the included
example ( example.py ).

Due to the inherent unpredictability of the demands imposed by the various
-Omics (as in genomics or metabolomics, etc.) projects using BNOmics, it is
meant to serve as a prototypical research platform, modified upon necessity to
address the HPC needs, rather than a narrow purpose, typical desktop
application.


Requirements:
Python interpreter - required.
Numpy module - required. 
Graphviz - optional but recomended for graphical rendering. 



Example script:
To start with the example please open a terminal and navigate to the BNOmics
folder. Once there, you can call example.py as a standard python script with a
filename argument:

>>python example.py african_americans.csv

The two example data files african_americans.csv and european_americans.csv are
provided in the collection.

After the execution of example.py completes, the structure of reconstructed BN
will be saved in dotfile.dot and can be rendered with graphviz as follows:

>>dot -Tpdf dotfile.dot -o outpdf.pdf

If Graphviz is properly installed the rendering procedure will be called
automatically generating outpdf.pdf upon execution of example.py , and the above
manual invocation of the rendering procedure will not be neccessary.

Now you can open outpdf.pdf with any pdf viewer for investigation of the
results.

Feel free to open example.py with your editor of choice and view the contents.
This file contains the most typical and simple example of a workflow for data
driven BN reconstruction. This little script can be easily modified and tuned
using the comments provided in the file.


Interactive use:
In an interactive environment you can usually examine the contents of the
included files as follows:

>>import bnomics
>>help(bnomics)

The typical workflow will be identical to the example.py script with the
additional benefit of further details and information available for
examination. For example, a BN can be modified by hand, its structure can be
viewed as a list, a different search method can be applied or even constructed,
etc. 

#//=============================================================
#//(c) 2011 Distributed under MIT-style license. 
#//(see LICENSE.txt or visit http://opensource.org/licenses/MIT)
#//=============================================================
