import pkg_resources
import logging
import subprocess

_logger = logging.getLogger("regal_synthesis")
_logger.addHandler(logging.NullHandler())

_logger_yosys = logging.getLogger("yosys")
_logger_yosys.addHandler(logging.NullHandler())


def synth(outfile, *infiles, **kwargs):
    _logger.info("Synthesis")
    yosys_commands = []

    gal_lib = pkg_resources.resource_filename("regal.synth", "gal.v")
    tri_file = pkg_resources.resource_filename("regal.synth", "gal_tri.v")
    yosys_commands += [
        "read_verilog -lib {}".format(gal_lib),
        "read_verilog -lib {}".format(tri_file),
        "hierarchy -check -top top",
        "proc",
        "opt"
    ]

    map_file = pkg_resources.resource_filename("regal.synth", "gal_map.v")
    yosys_commands += [
        "extract -map {}".format(tri_file),
        "opt",
        "techmap",
        "opt",
        "abc -sop -P 8 -I 8",
        "opt",
        "techmap -map {}".format(map_file),
        "opt",
        "clean"
    ]

    if kwargs.get("show", False):
        yosys_commands.append("show -viewer xdot -format dot")

    yosys_commands = "; ".join(yosys_commands)
    res = subprocess.run(["yosys",
        "-f", "verilog",
        "-b", "json",
        "-o", outfile,
        "-p", yosys_commands] + list(infiles),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    for line in res.stdout.decode("utf-8").split("\n"):
        _logger_yosys.debug(line)
    for line in res.stderr.decode("utf-8").split("\n"):
        if line != "":
            _logger_yosys.error("{}".format(line))

    return res.returncode == 0
