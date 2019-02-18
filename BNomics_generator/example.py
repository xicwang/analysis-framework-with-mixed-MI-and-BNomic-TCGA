#//=============================================================
#//(c) 2011 Distributed under MIT-style license. 
#//(see LICENSE.txt or visit http://opensource.org/licenses/MIT)
#//=============================================================

# Do not modify next 6 lines
import bnomics
import sys

# First load the datafile
filename=sys.argv[1]
dt=bnomics.dutils.loader(filename)

# Modifications possible below

##############################
# Now discretize the variables with
dt.discretize_all()

# Other options include 
# dt.bin_discretize(var_list=[1,2,3],bins=3)
# which takes a list of variables and bin number as arguments.
# To discretize 1st, 2nd, and 3rd variables (count is from 0) do
# dt.bin_discretize([1,2,3])
# To discretize a range of variables [i,...,j], you can use the command
# range(i,j+1) like so
# dt.bin_discretize(range(1,11))


#######################
# Initialize the search
srch=bnomics.search(dt)

# Parameters for the objective function (metric)
# can be added to the search argument list like so
# srch=bgen.search(dt,'mdl')
# The default is 'bdm'
# If ofext.cpp is compiled 'cmdla' and 'cmdlb' represent a faster alternative


####################
# Perform the search
srch.gsrestarts()

# There are 2 arguments that can be passed into the gsrestarts function
# nrestarts - number of restarts performed during the search
# tol - lower bound of the numerical tolerance
# Both arguments are used as a stopping criterion for the searchin algorithm.


################################################################################
# Save the reconstructed BN structure in dotfile.dot and generate a rendering of
# the result in outpdf.pdf (if Graphviz is properly installed).
srch.dot()

# Another option is to save only a Markov neighborhood of some variable
# srch.dot(cnode=6)
# for example


