import csv
import json
import logging
from quine_mccluskey.qm import QuineMcCluskey
from multiprocessing import Pool

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
    qm = QuineMcCluskey()
    _tt_simplified = qm.simplify(entries)
    _logger.debug("%s = %s", name, _tt_simplified)
    return _tt_simplified


def tt2v(infile, outfile):
    tt = {}

    with open(infile, "r") as f:
        ttreader = csv.reader(f)
        inputs, outputs = read_io_names(next(ttreader))

        for output in outputs:
            tt[output] = []

        output_base = len(inputs) + 1
        for row in ttreader:
            for output_idx, output_name in enumerate(outputs):
                if int(row[output_base + output_idx]):
                    input_values = int("".join(row[0:len(inputs)]), 2)
                    if output_name not in tt.keys():
                        tt[output_name] = []
                    tt[output_name].append(input_values)


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
            ports.append("    output {}".format(output))
        f.write(",\n".join(ports))
        f.write("\n);\n\n")

        for output, entries in zip(outputs, tt_simplified):
            f.write("assign {} =\n".format(output))
            if entries is None:
                f.write("  0\n;\n\n")
                continue

            sop = []
            for entry in sorted(entries):
                line = []
                entry = "0" * (len(inputs) - len(entry)) + entry
                for i in range(len(inputs)):
                    c = entry[i]
                    if c != "-":
                        line.append("{}{}".format(
                            "" if c == "1" else "~",
                            inputs[i]
                        ))
                if line != []:
                    sop.append("  ({})".format(" & ".join(line)))
                else:
                    sop.append("  1")
            f.write("{}\n;\n\n".format(" |\n".join(sop)))

        f.write("endmodule\n")

    return True
