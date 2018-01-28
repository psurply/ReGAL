import logging
import yaml

from regal.pnr.exception import PnrError
from regal.pnr.netlist import Netlist
from regal.pnr.gal import Gal16v8, Gal20v8

_logger = logging.getLogger("regal_pnr")
_logger.addHandler(logging.NullHandler())

_devices = {
    "GAL16V8": Gal16v8,
    "GAL20V8": Gal20v8,
}

def pnr(netlist, cfgfile, outfile, top="top"):
    _logger.info("Starting Place-and-route")

    with open(cfgfile, "r") as f:
        cfg = yaml.load(f)

    try:
        netlist = Netlist(netlist, top)

        try:
            gal = _devices[cfg["device"]](cfg["mode"])
        except KeyError:
            _logger.error("Supported devices: %s", ",".join(_devices.keys()))
            raise PnrError("Invalid target: {}".format(target))

        gal.pnr(netlist, cfg["pins"])

        _logger.info("Place-and-route succeed")
    except PnrError as exc:
        _logger.error(exc)
        return False

    with open(outfile, "w+") as f:
        _logger.info("Producing JEDEC file to {}".format(outfile))
        gal.write_jedec(f)

    return True
