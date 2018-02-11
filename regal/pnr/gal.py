import logging
import sys

from datetime import datetime

from regal.pnr.exception import PnrError
from regal.pnr.jedec import Jedec

_logger = logging.getLogger("regal_pnr")
_logger.addHandler(logging.NullHandler())


class Cell:
    def __init__(self, gal_mode, outpad, inputs, depth=8):
        self.gal_mode = gal_mode
        self.outpad = outpad
        self.inputs = inputs
        self.depth = depth
        self.width = len(inputs) * 2

        self.fuses_and_array = [1] * self.width * self.depth
        self.fuses_ptd = [1] * depth
        self.fuse_xor = 0

        if self.gal_mode == "registered":
            self.fuse_ac1 = 1
        else:
            self.fuse_ac1 = 0

        self.used = False

    def _connect_input(self, netname, pins, table):
        _logger.info("Connecting input %s to macro cell %d", netname, self.outpad)
        try:
            inpad = pins[netname]
        except KeyError:
            raise PnrError("No IO assigned for netname {}".format(netname))

        try:
            index_input = self.inputs.index(inpad)
        except ValueError:
            raise PnrError("Pad {} cannot be assigned as input".format(inpad))
        _logger.debug("Position of netname %s: %d", netname, index_input)

        for i in range(self.depth - int(self.has_oe())):
            idx = (i + int(self.has_oe())) * self.width + (index_input * 2)
            self.fuses_and_array[idx] = table[i * 2] ^ 1
            self.fuses_and_array[idx + 1] = table[i * 2 + 1] ^ 1

    def _get_input_table(self, sop, index):
        sop_table = sop["parameters"]["TABLE"]
        sop_depth = sop["parameters"]["DEPTH"]
        sop_width = sop["parameters"]["WIDTH"]

        table = []
        for i in range(index * 2, self.depth * sop_width * 2, sop_width * 2):
            table.append((sop_table >> (i + 1) & 1))
            table.append((sop_table >> i & 1))

        _logger.debug("Input table %d: %s", index, table)
        return table

    def configure_and_array(self, netlist, sop, pins):
        _logger.info("Configuring AND-array for macro cell {}".format(self.outpad))

        for input_name, connection in sop["connections"].items():
            if not input_name.startswith("I"):
                continue
            index = int(input_name[1:])
            connection = connection[0]
            if connection != "0":
                netname = netlist.get_netname(connection)
                self._connect_input(netname, pins,
                                    self._get_input_table(sop, index))

    def invert(self):
        _logger.info("Inverting output of macro cell %s", self.outpad)
        self.fuse_xor = 0

    def set_registered(self, clock, pins):
        _logger.info(
            "Configure macro cell %s in registered mode (clock: %s)",
            self.outpad, clock
        )
        if self.gal_mode != "registered":
            raise PnrError(
                "GAL_DFF can only be synthesized in registered mode"
                " (current GAL mode: {})".format(self.gal_mode)
            )

        sysclk = None
        for netname, pin in pins.items():
            if pin == 1:
                sysclk = netname

        if clock != sysclk:
            raise PnrError(
                "{} is not mapped to a clock input "
                "(currently mapped to {} signal)".format(clock, sysclk)
            )
        self.fuse_ac1 = 0

    def has_oe(self):
        return self.gal_mode == "registered" and self.fuse_ac1

    def configure(self, netlist, bit, pins):
        _logger.info("Configuring macro cell {}".format(self.outpad))

        self.fuse_xor = 1

        if type(bit) is int:
            driver = netlist.get_driver(bit)

            if driver["type"] == "GAL_DFF":
                clock = netlist.get_netname(driver["connections"]["C"][0])
                self.set_registered(clock, pins)
                driver = netlist.get_driver(driver["connections"]["D"][0])

            if driver["type"] == "GAL_XOR":
                self.invert()
                driver = netlist.get_driver(driver["connections"]["A"][0])

            if driver["type"] == "GAL_SOP":
                self.configure_and_array(netlist, driver, pins)
            else:
                raise PnrError("Unknown cell type: {}".format(driver["type"]))
        elif bit == "1":
            self.invert()
        elif bit != "0":
            raise PnrError("Cannot assign value {} to outpad {}".format(
                bit, self.outpad
            ))

        self.used = True


class Gal:
    def __init__(self, mode, inpads, outpads):
        self.inpads = inpads
        self.outpads = outpads
        self.mode = mode

        self.fuses_signature = [0] * 64
        if mode == "registered":
            self.fuse_syn = 0
            self.fuse_ac0 = 1
        elif mode == "complex":
            self.fuse_syn = 1
            self.fuse_ac0 = 1
        elif mode == "simple":
            self.fuse_syn = 1
            self.fuse_ac0 = 0
        else:
            raise ValueError("Invalid GAL mode: {}".format(mode))

        self.cells = []
        for outpad in outpads:
            self.cells.append(Cell(mode, outpad, self.inpads))

        _logger.info("GAL%dV%d configured in %s mode",
                     len(inpads), len(outpads), mode)

    def get_cell(self, outpad):
        for cell in self.cells:
            if cell.outpad == outpad:
                return cell
        raise KeyError

    def pnr(self, netlist, pins):
        for netname, pin in netlist.get_outputs(pins):
            cell = self.get_cell(pin)
            if cell.used:
                raise PnrError("Cell {} is already used".format(pin))

            bit = netlist.get_bit(netname)
            cell.configure(netlist, bit, pins)


class GalXXv8(Gal):
    def write_jedec(self, stream):
        offset = 0

        design_specs = """
    Generated by ReGAL
    Device: {}
""".format(type(self).__name__)

        jedec = Jedec(stream, design_specs)
        jedec.fuse_number(self.fuse_number)
        jedec.fuse_default(0)
        jedec.security_fuse(0)

        # AND-array
        for cell in self.cells:
            jedec.comment("Macro cell {} AND-Array".format(cell.outpad))

            for line_idx in range(0, cell.width * cell.depth, cell.width):
                line = cell.fuses_and_array[line_idx:line_idx + cell.width]
                if 0 in line or (cell.has_oe() and line_idx == 0):
                    offset = jedec.fuses(offset, line)
                else:
                    offset += cell.width

        # XOR
        for cell in self.cells:
            jedec.comment("Macro cell {} XOR".format(cell.outpad))
            offset = jedec.fuses(offset, [cell.fuse_xor])

        # Signature
        jedec.comment("Signature")
        offset = jedec.fuses(offset, self.fuses_signature)

        # AC1
        for cell in self.cells:
            jedec.comment("Macro cell {} AC1".format(cell.outpad))
            offset = jedec.fuses(offset, [cell.fuse_ac1])

        # PTD
        for cell in self.cells:
            jedec.comment("Macro cell {} PTD".format(cell.outpad))
            offset = jedec.fuses(offset, cell.fuses_ptd)

        # SYN / AC0
        jedec.comment("SYN")
        offset = jedec.fuses(offset, [self.fuse_syn])
        jedec.comment("AC0")
        offset = jedec.fuses(offset, [self.fuse_ac0])

        jedec.checksum()


class Gal16v8(GalXXv8):
    def __init__(self, mode):
        self.fuse_number = 2194

        inpads = []
        outpads = []
        if mode == "simple":
            inpads = [
                2,  1, 3, 19,
                4, 18, 5, 17,
                6, 14, 7, 13,
                8, 12, 9, 11
            ]
            outpads = [19, 18, 17, 16, 15, 14, 13, 12]
        elif mode == "registered":
            inpads = [
                2, 19, 3, 18,
                4, 17, 5, 16,
                6, 15, 7, 14,
                8, 13, 9, 12
            ]
            outpads = [19, 18, 17, 16, 15, 14, 13, 12]

        GalXXv8.__init__(self, mode, inpads, outpads)


class Gal20v8(GalXXv8):
    def __init__(self, mode):
        self.fuse_number = 2706

        inpads = []
        outpads = []
        if mode == "simple":
            inpads = [
                 2,  1,  3, 23,
                 4, 22,  5, 21,
                 6, 20,  7, 17,
                 8, 16,  9, 15,
                10, 14, 11, 13
            ]
            outpads = [22, 21, 20, 19, 18, 17, 16, 15]

        GalXXv8.__init__(self, mode, inpads, outpads)
