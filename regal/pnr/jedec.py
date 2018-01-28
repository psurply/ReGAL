import logging

_logger = logging.getLogger("regal_jedec")
_logger.addHandler(logging.NullHandler())

STX = "\x02"
ETX = "\x03"


class Jedec:
    def __init__(self, stream, design_specs=""):
        self.stream = stream
        self._fuses = []
        self._fuse_number = 0
        self._fuse_default = 0
        self._content = ""

        self.stream.write(STX)
        self.out("\r\n" + design_specs + "*")

    def init_fuses(self):
        self._fuses = [self._fuse_default] * self._fuse_number

    def out(self, cmd):
        _logger.debug("%s", cmd)
        line = cmd + "\r\n"
        self.stream.write(line)
        self._content += line

    def comment(self, comment):
        self.out("N {} *".format(comment))

    def fuse_default(self, fuse_default):
        self._fuse_default = fuse_default
        self.out("F{} *".format(fuse_default))
        self.init_fuses()

    def security_fuse(self, value):
        self.out("G{} *".format(value))

    def fuse_number(self, fuse_number):
        self._fuse_number = fuse_number
        self.out("QF{} *".format(fuse_number))
        self.init_fuses()

    def fuses(self, offset, fuses):
        for idx, fuse in enumerate(fuses):
            self._fuses[offset + idx] = fuse
        fuses = "".join([str(fuse) for fuse in fuses])
        self.out("L{:04d} {} *".format(offset, fuses))
        return offset + len(fuses)

    def checksum(self):
        word_size = 8
        checksum = 0
        for i in range(0, self._fuse_number, word_size):
            word = 0
            for j in range(word_size):
                if i + j >= self._fuse_number:
                    break
                word |= self._fuses[i + j] << j
            checksum += word
        checksum &= 0xFFFF
        self.out("C{:04X} *".format(checksum))

        file_checksum = 0
        for c in self._content:
            file_checksum += ord(c)
        file_checksum += 0x03
        file_checksum &= 0xFFFF
        self.stream.write(ETX + "{:04X}".format(file_checksum))
