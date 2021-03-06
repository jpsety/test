"""
Python package `circuitgraph` provides a data structure
for the generation, manipulation, and evaluation of
Boolean circuits. The circuits are represented in a graph
format based on the `networkx` package.

Features include:

- parsing of generic verilog modules
- easy circuit composition
- synthesis interface to Genus and Yosys
- SAT,#SAT, and approx-#SAT solver integration via `pysat` and `approxmc`
- implementations of common circuit transformations

"""

from circuitgraph.circuit import *
from circuitgraph.io import *
from circuitgraph.sat import *
from circuitgraph.sim import *
from circuitgraph.transform import *
from circuitgraph.logic import *
