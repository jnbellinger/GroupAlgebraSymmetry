# GroupAlgebraSymmetry
Find commutation relations for differential transforms in a group algebra over a finite non-abelian group
In the paper "Symmetries of preon interactions modeled as a finite group" 
(J.N. Bellinger J.Math.Phys.38: 3414-3426,1997), I showed that
non-abelian finite groups can sustain a special type of 
continuous transformations in a group algebra space, one in which
each transform maps the group elements
in such a way that the result new "elements" maintain the original group structure.
This is in addition to the obvious
permutations possible among elements of the finite group.

The question I want to answer is **"Is there a simple way to predict from aspects of the finite group what those
symmetries will be?"**

I find that examples make analysis easier, so I am providing some tools for generating
the symmetries.  It expects a finite group presented as a text Cayley table with elements
numbered from 0 to N-1.

This python program generates a set of commutation relations among the differential
transformations, but does not attempt to resolve which continuous groups these might be.
I don't know a systematic procedure for comparing sets of commutation relations to find
if the sets are equivalent--and would be very interested in hearing about such things.



Pull the tree from GitHub.
----------

Test a few things.

* pip install coverage
* coverage run -m unittest tests/test_*.py
* coverage html
* python3 Builder/run.py tests/a4group

Several non-abelian finite groups are provided as examples in the tests/ directory, such as the a4group
referenced above.  For example, the file _tests/6group_ is just

0 1 2 3 4 5 \
1 2 0 4 5 3 \
2 0 1 5 3 4 \
3 5 4 0 2 1 \
4 3 5 1 0 2 \
5 4 3 2 1 0

Its symmetries are generated by 3 differential transformations, the commutators of whose
matrices are

[C0, C1] = (-2)C2 \
[C0, C2] = (-2)C1 \
[C1, C2] = (2)C0

The _tests/a4group_ example has 8 generators, and 28 commutation relations, which can be manually
simplified if you please.


Limitations
------

This is not lightning-fast.  You will probably not have the patience to wait for a set of commutators
even when the group size is well less than the implied size limit of 100.  The a4group example takes
a minute and a half on my machine.  The 16_9group example takes a little over 9 minutes.

The equation-solving is simple, and I do not warrant that it will be adequate for all situations
arising.  If it isn't adequate, one can try using lapack instead of exact fractions, and rounding off
the numbers when done.  I probably should have taken that approach from the beginning, but was worried
that there might be stability issues which, combined with the rounding, would give me bogus answers.

The approach I used working on the original paper used a Fortran program to create and pre-simplify
the equations, but the final solution and creation of commutation relations was manual.

Contents
------
The *Builder* directory contains the python source files.

The *docs* directory contains a couple of LaTeX files:  the original results collection (not
the same as the shorter JMP paper, and **not** cross-checked.  E.g. example 16_9 is different
from the result I get with this program) and an as-yet unpublished paper on transformations of
dihedral groups.  (Executive summary:  a dihedral group of order **p** has at most **3(p-1)/2**
generators if **p** is odd, and **3(p-2)/2** generators if **p** is even.)

The *tests* directory contains python testing files (it does not have 100% coverage) for use with
the *coverage* tool, and a few example group Cayley tables.  Please do not laugh too hard at the
code.
