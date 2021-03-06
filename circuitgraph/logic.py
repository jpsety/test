"""A collection of common logic elements as `CircuitGraph` objects"""
from circuitgraph import Circuit, clog2
from itertools import product


def adder(w):
    """
    Create an adder.

    Parameters
    ----------
    w: the width of the adder.

    Returns
    -------
    a `CircuitGraph` addder.
    """
    c = Circuit(name="adder")
    carry = c.add("null", "0")
    for i in range(w):
        # sum
        c.add(f"a_{i}", "input")
        c.add(f"b_{i}", "input")
        c.add(f"out_{i}", "xor", fanin=[f"a_{i}", f"b_{i}", carry],
              output=True)

        # carry
        c.add(f"and_ab_{i}", "and", fanin=[f"a_{i}", f"b_{i}"])
        c.add(f"and_ac_{i}", "and", fanin=[f"a_{i}", carry])
        c.add(f"and_bc_{i}", "and", fanin=[f"b_{i}", carry])
        carry = c.add(
            f"carry_{i}", "or", fanin=[f"and_ab_{i}", f"and_ac_{i}", f"and_bc_{i}",]
        )

    c.add(f"out_{w}", "buf", fanin=carry, output=True)
    return c


def mux(w):
    """
    Create a mux.

    Parameters
    ----------
    w: the width of the mux.

    Returns
    -------
    a `CircuitGraph` mux.
    """
    c = Circuit(name="mux")

    # create inputs
    for i in range(w):
        c.add(f"in_{i}", "input")
    sels = []
    for i in range(clog2(w)):
        c.add(f"sel_{i}", "input")
        c.add(f"not_sel_{i}", "not", fanin=f"sel_{i}")
        sels.append([f"not_sel_{i}", f"sel_{i}"])

    # create output or
    c.add("out", "or", output=True)

    i = 0
    for sel in product(*sels[::-1]):
        c.add(f"and_{i}", "and", fanin=[*sel, f"in_{i}"], fanout="out")

        i += 1
        if i == w:
            break

    return c


def popcount(w):
    """
    Create a population count circuit.

    Parameters
    ----------
    w: the width of the adder.

    Returns
    -------
    a `CircuitGraph` addder.
    """
    c = Circuit(name="popcount")
    ps = [[c.add(f"in_{i}", "input")] for i in range(w)]
    c.add("null", "0")

    i = 0
    while len(ps) > 1:
        # get values
        ns = ps.pop(0)
        ms = ps.pop(0)

        # pad
        aw = max(len(ns), len(ms))
        while len(ms) < aw:
            ms += ["null"]
        while len(ns) < aw:
            ns += ["null"]

        # instantiate and connect adder
        a = adder(aw).strip_io()
        c.extend(a.relabel({n: f"add_{i}_{n}" for n in a.nodes()}))
        for j, (n, m) in enumerate(zip(ns, ms)):
            c.connect(n, f"add_{i}_a_{j}")
            c.connect(m, f"add_{i}_b_{j}")

        # add adder outputs
        ps.append([f"add_{i}_out_{j}" for j in range(aw + 1)])
        i += 1

    # connect outputs
    for i, o in enumerate(ps[0]):
        c.add(f"out_{i}", "buf", fanin=o, output=True)

    return c

def comb_lat():
    lm = Circuit(name='lat')

    # mux
    m = logic.mux(2).strip_io()
    lm.extend(m.relabel({n: f'mux_{n}' for n in m.nodes()}))

    # inputs
    lm.add("si", "input", fanout="mux_in_0")
    lm.add("d", "input", fanout="mux_in_1")
    lm.add("clk", "input", fanout="mux_sel_0")
    lm.add("r", "input")
    lm.add("s", "input")

    # logic
    lm.add("r_b", "not", fanin="r")
    lm.add_node("qr", gate="and", fanin=["mux_out","r_b"])
    lm.add_node("q", gate="or", fanin=["qr","s"],
                output=True)
    lm.add_node("so", gate="buf", fanin="q", output=True)

    return lm

def comb_ff():
    lm = Circuit(name='ff')

    # mux
    m = logic.mux(2).strip_io()
    lm.extend(m.relabel({n: f'mux_{n}' for n in m.nodes()}))

    # inputs
    lm.add("si", "input", fanout="mux_in_0")
    lm.add("d", "input", fanout="mux_in_1")
    lm.add("clk", "input", fanout="mux_sel_0")
    lm.add("r", "input")
    lm.add("s", "input")

    # logic
    lm.add("r_b", "not", fanin="r")
    lm.add_node("qr", gate="and", fanin=["mux_out","r_b"])
    lm.add_node("q", gate="or", fanin=["qr","s"],
                output=True)
    lm.add_node("so", gate="buf", fanin="q", output=True)

    return lm
