import argparse
import logging
import sys
import tempfile

from regal.dump import dump, tt2v
from regal.pnr import pnr
from regal.synth import synth


_default_netlist_file = "netlist.json"
_default_jedec_file = "fuses.jed"
_default_dump_device = "/dev/ttyACM0"


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.set_defaults(action="")
    subparser = parser.add_subparsers()

    synth_parser = subparser.add_parser(
        name="synth",
        help="synthesize a verilog file into a netlist (requires yosys)"
    )
    synth_parser.add_argument("-o", "--outfile", default=_default_netlist_file)
    synth_parser.add_argument("-s", "--show", action="store_true")
    synth_parser.add_argument("rtl", nargs="+")
    synth_parser.set_defaults(action="synth")

    pnr_parser = subparser.add_parser(
        name="pnr",
        help="place-and-route a netlist and output a JEDEC file"
    )
    pnr_parser.add_argument("-o", "--outfile", default=_default_jedec_file)
    pnr_parser.add_argument("-t", "--top", default="top")
    pnr_parser.add_argument("config")
    pnr_parser.add_argument("netlist", default=_default_netlist_file)
    pnr_parser.set_defaults(action="pnr")

    build_parser = subparser.add_parser(
        name="build",
        help="synthesize and place-and-route a verilog design"
    )
    build_parser.add_argument("-o", "--outfile", default=_default_jedec_file)
    build_parser.add_argument("-t", "--top", default="top")
    build_parser.add_argument("config")
    build_parser.add_argument("rtl", nargs="+")
    build_parser.set_defaults(action="build")

    dump_parser = subparser.add_parser(
        name="dump",
        help="dump the truth-table from a PAL"
    )
    dump_parser.add_argument("config")
    dump_parser.set_defaults(action="dump")

    tt2v_parser = subparser.add_parser(
        name="tt2v",
        help="simplify and convert a truth-table to a verilog file"
    )
    tt2v_parser.add_argument("infile")
    tt2v_parser.add_argument("outfile")
    tt2v_parser.set_defaults(action="tt2v")

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    loglevels = [logging.WARN, logging.INFO, logging.DEBUG]
    if args.verbose >= len(loglevels):
        args.verbose = len(loglevels) - 1

    logging.basicConfig(stream=sys.stderr, level=loglevels[args.verbose],
            format='[%(levelname)s][%(name)s] %(message)s')

    logging.addLevelName(logging.DEBUG,   "\033[1;34mDEBUG\033[1;0m")
    logging.addLevelName(logging.INFO,    "\033[1;32mINFO \033[1;0m")
    logging.addLevelName(logging.WARNING, "\033[1;33mWARN \033[1;0m")
    logging.addLevelName(logging.ERROR,   "\033[1;31mERROR\033[1;0m")

    if args.action == "build":
        netlist_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        netlist = netlist_file.name
        netlist_file.close()

        if not synth(netlist, *args.rtl):
            sys.exit(1)
        if not pnr(netlist, args.config, args.outfile, args.top):
            sys.exit(1)
    elif args.action == "synth":
        if not synth(args.outfile, *args.rtl, show=args.show):
            sys.exit(1)
    elif args.action == "pnr":
        if not pnr(args.netlist, args.config, args.outfile, args.top):
            sys.exit(1)
    elif args.action == "dump":
        if not (dump(args.config)):
            sys.exit(1)
    elif args.action == "tt2v":
        if not (tt2v(args.infile, args.outfile)):
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
