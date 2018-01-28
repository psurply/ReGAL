import os
import pytest
import json
import regal


_samples = [
    ("and.v", "and.jed"),
    ("nand.v", "nand.jed"),
    ("not.v", "not.jed"),
    ("or.v", "or.jed"),
    ("xor.v", "xor.jed"),
    ("v1.v", "v1.jed"),
    ("v0.v", "v0.jed"),
    ("fb.v", "fb.jed"),
]


@pytest.mark.parametrize("rtl,jedec", _samples)
def test_synth(tmpdir, rtl, jedec):
    netlist = tmpdir.join("netlist.json")
    regal.synth(str(netlist), os.path.join("tests", "samples", rtl))

    out = tmpdir.join("out.jed")
    cfg = os.path.join("tests", "samples", "device.yaml")
    regal.pnr(str(netlist), cfg, str(out))

    with open(os.path.join("tests", "samples", jedec), "r") as f:
        assert f.read() == out.read()
