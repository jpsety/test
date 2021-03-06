--- 
title: 'CircuitGraph: A Python package for Boolean circuits'
tags:
  - Python
  - Boolean circuits
  - satisfiability
  - graph
  - electronic design automation
authors:
  - name: Joseph Sweeney
    affiliation: 1
  - name: Ruben Purdy
    affiliation: 1
affiliations:
  - name: Carnegie Mellon University
    index: 1
date: 13 August 2020
bibliography: paper.bib

--- 

# Summary

A Boolean circuit is a fundamental mathematical model ubiquitous to the 
design of modern computers. The model consists of a directed graph wherein 
nodes are logic gates with corresponding Boolean functions and edges are wires 
which determine the composition of the gates. `CircuitGraph` is a open-source Python library
for manipulating and analyzing Boolean circuits. 

# Statement of need 

Highly optimized software for processing Boolean circuits exists. Unfortunately
it generally is proprietary, with expensive license fees. Furthermore, these
options suffer from poor documentation, are closed source, and typically 
rely on Tool control language (Tcl). While simple, Tcl is slow, has limited
libraries and supporting community, and is unecessarily verbose. These reasons
motivate the development of our open source solution. While this software will 
directly benefit our lab as a research platform, it certainly has application 
in other environments such as the classroom.

# Functionality

The functionality of `CircuitGraph` has been tailored to our research needs, however,
the library is easily extensible to many other applications of Boolean circuits.

The core of the library is the `Circuit` class, which internally uses a `networkx.DiGraph` 
as the fundamental data structure. The class implements key Boolean circuit functionalities 
on top of the graph. 

## Interfaces

Compatibility with existing systems is a primary goal for our library. Towards this end, 
we have built interfaces for the commonly used Boolean circuit formats: Bench and Verilog.
Additionally, we plan on supporting BLIF. The user is able to import and export in the supported
formats, enabling interfacing with other tools as well as conversion between formats.
We also have provided a library of generic and benchmark circuits that can be quickly instantiated.

```python
import circuitgraph as cg
c0 = cg.from_file('path/circuit.v')
c1 = cg.from_file('path/circuit.bench')
c2 = cg.from_lib('c17')
```	

## Concise Composition

A common issue found in similar tools is the poor expressivity of circuit construction 
primitives. We aim to build a simple, but powerful syntax for creating and connecting nodes
in a circuit. The ease of our syntax is enabled by the python language. 
An example of this syntax is below.

```python
# add an OR gate named 'a'
c0.add('a','or')

# create an AND with circuit inputs in a single line
c0.add('g','and',fanin=[c.add(f'in_{i}','input') for i in range(4)])
```	

## Synthesis


## Satisfiability

Satisfiablility is an essential problem related to Boolean circuits. Suprisingly, commercial 
synthesis tools do not directly support its use (although the open source tools yosys does). 
We add satisfiability to our library which in turn enables a wide array of analysis including
sensitization, sensitivity, and influence. Our implementation allows a simple interface to determine
satisfiability of a circuit under a set of variable assignments. To develop more complex routines, the
user can also access the underlying `pysat.solver` instance. 
In conjunction with satisfiability, we provide interfaces to approximate and exact model count algorithms. 

```python
# check satisfiability assuming 'a' is False
cg.sat(c0,{'a':False})

# get number of solutions to circuit with 'a' False
cg.model_count(c0,{'a':False})
```	

# Acknowledgements

We acknowledge ...


