import csv
import logging
import serial
import time

_logger = logging.getLogger("regal_dump")
_logger.addHandler(logging.NullHandler())


_port_offsets = {
    "C": 0,
    "L": 1,
    "A": 2,
}

def _read_entry(ser):
    while ser.read() != b'\x02':
        continue

    payload = []
    for byte in ser.read(3):
        payload.append(byte)

    return payload


def _get_input_state(payload, output_mask, fixed_input_size):
    out = 0
    offset = 0

    for i in range(8):
        if (output_mask >> i) & 1:
            out |= ((payload[2] >> i) & 1) << offset;
            offset += 1

    return payload[0] | (payload[1] << 8) | (out << fixed_input_size)


def _get_output_state(payload, output_mask):
    out = 0
    offset = 0

    for i in range(8):
        if ((output_mask >> i) & 1) == 0:
            out |= ((payload[2] >> i) & 1) << offset;
            offset += 1

    return out


def _get_pin_state(payload, pin):
    port = pin[0]
    offset = int(pin[1])

    return (int(payload[_port_offsets[port]]) >> offset) & 1


def dump(outfile, device, io):
    _logger.info("Dumping truth-table")

    start = 0
    fixed_input_size = len(io["inputs"])
    output_mask = 0

    input_size = fixed_input_size
    for i in range(8):
        if ((output_mask >> i) & 1):
            input_size += 1

    end = (2 ** input_size)

    with serial.Serial(device, 115200, timeout=2) as ser:
        with open(outfile, "w+") as f:
            ttwriter = csv.writer(f)
            header = []
            for input in io["inputs"]:
                for input_name in input.keys():
                    header.append(input_name)
            header.append("")
            for output in io["outputs"]:
                for output_name in output.keys():
                    header.append(output_name)
            ttwriter.writerow(header)

            time.sleep(2)
            ser.write(b'ssssss')
            ser.flushInput()
            ser.write(bytes([ord("d"), output_mask]))
            ser.write(bytes([
                ord("r"),
                (start >> 24) & 0xFF,
                (start >> 16) & 0xFF,
                (start >> 8) & 0xFF,
                start & 0xFF
            ]))

            ser.write(b'p')

            percent = 0

            for i in range(start, end):
                payload = _read_entry(ser)
                while _get_input_state(payload, output_mask, fixed_input_size) != i:
                    _logger.warn("Expected entry %x, got %x",
                                 i, _get_input_state(payload,
                                                     output_mask,
                                                     fixed_input_size))
                    payload = _read_entry(ser)

                #f.write("{:06x} {:02x}\n".
                #        format(i, _get_output_state(payload, output_mask)))
                row = []
                for input in io["inputs"]:
                    for pin in input.values():
                        row.append(_get_pin_state(payload, pin))
                row.append("")
                for output in io["outputs"]:
                    for pin in output.values():
                        row.append(_get_pin_state(payload, pin))
                ttwriter.writerow(row)

                p = int((i / end) * 100. + 1)
                if p != percent:
                    percent = p
                    _logger.info("%d %% (%06x)", percent, i)

    return True
