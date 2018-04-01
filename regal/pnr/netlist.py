import logging
import json

from regal.pnr.exception import PnrError

_logger = logging.getLogger("regal_pnr")
_logger.addHandler(logging.NullHandler())


class Netlist:
    def __init__(self, infile, top):
        with open(infile, "r") as f:
            self.netlist = json.load(f)
        self.top = self.netlist["modules"][top]

    def get_bits(self, netname):
        return self.top["netnames"][netname]["bits"]

    def get_bit(self, netname):
        bits = self.get_bits(netname)
        if len(bits) != 1:
            raise PnrError("Wire {} must be exactly 1 bit (is {})".
                           format(netname, len(bits)))
        return bits[0]

    def get_driver(self, bit):
        for cell_name, cell in self.top["cells"].items():
            for connection_name, bits in cell["connections"].items():
                if bit in bits and \
                   cell["port_directions"][connection_name] == "output":
                       _logger.debug(
                            "Found driver for bit %d: %s",
                            bit, cell_name
                        )
                       return cell
        raise PnrError("Cannot find a driver for bit {}".format(bit))

    def get_netname(self, bit):
        for name, netname in self.top["netnames"].items():
            if bit in netname["bits"]:
                return name
        raise PnrError("Cannot find netname for bit {}".format(bit))

    def get_ios(self, pins):
        for netname, pin in pins.items():
            try:
                port = self.top["ports"][netname]
            except KeyError:
                _logger.warning("Port {} not assigned. Ignored".format(netname))
                continue

            yield netname, pin, port["direction"]
