import csv
import json
import logging
from quine_mccluskey.qm import QuineMcCluskey
from multiprocessing import Pool
from collections import defaultdict

_logger = logging.getLogger("regal_dump")
_logger.addHandler(logging.NullHandler())


def read_io_names(header):
    tmp = []
    for field in header:
        if field == "":
            inputs = tmp
            tmp = []
        else:
            tmp.append(field)
    outputs = tmp

    _logger.debug("Inputs: %s", inputs)
    _logger.debug("Outputs: %s", outputs)
    return (inputs, outputs)


def _simplify(expr):
    name, entries = expr
    _logger.debug("Simplifying %s...", entries)
    if entries == [0]:
        _tt_simplified = "0"
    else:
        qm = QuineMcCluskey()
        _tt_simplified = qm.simplify(entries)
    _logger.debug("%s: %s", name, _tt_simplified)
    return _tt_simplified


def tt2v(infile, outfile, clock=None, seq=[]):
    tt = defaultdict(list)

    with open(infile, "r") as f:
        ttreader = csv.reader(f)
        inputs, outputs = read_io_names(next(ttreader))

        for output in outputs:
            tt[output] = []

        output_base = len(inputs) + 1
        _row = [0] * (len(inputs) + len(outputs) + 1)
        if clock is not None:
            clk_idx = inputs.index(clock)

        for row in ttreader:
            for output_idx, output_name in enumerate(outputs):
                if output_name in seq and clock is not None:
                    # Clock rising edge
                    if int(row[clk_idx]) and not int(_row[clk_idx]) and \
                        int(row[output_base + output_idx]):
                        input_values = _row[output_base:]
                        input_values = int("".join(input_values), 2)
                        tt[output_name].append(input_values)
                elif int(row[output_base + output_idx]):
                    input_values = int("".join(row[0:len(inputs)]), 2)
                    tt[output_name].append(input_values)
            _row = row

    with Pool() as p:
        tt_simplified = p.map(
            _simplify,
            [(output, tt[output]) for output in outputs]
        )

    with open(outfile, "w+") as f:
        f.write("module top (\n")
        ports = []
        for input in inputs:
            ports.append("    input {}".format(input))
        for output in outputs:
            ports.append("    output {}{}".format(
                "reg " if output in seq else "",
                output
            ))
        f.write(",\n".join(ports))
        f.write("\n);\n\n")

        for output, entries in zip(outputs, tt_simplified):
            if output in seq:
                f.write("always @(posedge {})\n  {} <=\n".format(clock, output))
            else:
                f.write("assign {} =\n".format(output))
            if entries is None:
                f.write("  0\n;\n\n")
                continue

            sop = []
            for entry in sorted(entries):
                line = []
                if output in seq:
                    input_size = len(outputs)
                    input_names = outputs
                else:
                    input_size = len(inputs)
                    input_names = inputs
                entry = "0" * (input_size - len(entry)) + entry

                for i in range(input_size):
                    c = entry[i]
                    if c != "-":
                        input_name = input_names[i]
                        line.append("{}{}".format(
                            "" if c == "1" else "~",
                            input_name
                        ))
                if line != []:
                    sop.append("  ({})".format(" & ".join(line)))
                else:
                    sop.append("  1")
            f.write("{}\n;\n\n".format(" |\n".join(sop)))

        f.write("endmodule\n")

    return True
