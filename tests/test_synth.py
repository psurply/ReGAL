import os
import pytest
import json
import regal


_samples_simple = [
    ("and.v", "and.jed"),
    ("nand.v", "nand.jed"),
    ("not.v", "not.jed"),
    ("or.v", "or.jed"),
    ("xor.v", "xor.jed"),
    ("v1.v", "v1.jed"),
    ("v0.v", "v0.jed"),
    ("fb.v", "fb.jed"),
]

_samples_registered = [
    ("clk.v", "clk.jed"),
    ("clk_mixed.v", "clk_mixed.jed"),
]


@pytest.mark.parametrize("rtl,jedec", _samples_simple)
def test_synth_simple(tmpdir, rtl, jedec):
    netlist = tmpdir.join("netlist.json")
    regal.synth(str(netlist), os.path.join("tests", "samples", rtl))

    out = tmpdir.join("out.jed")
    cfg = os.path.join("tests", "samples", "device.yaml")
    regal.pnr(str(netlist), cfg, str(out))

    with open(os.path.join("tests", "samples", jedec), "r") as f:
        assert f.read() == out.read()


@pytest.mark.parametrize("rtl,jedec", _samples_registered)
def test_synth_registered(tmpdir, rtl, jedec):
    netlist = tmpdir.join("netlist.json")
    regal.synth(str(netlist), os.path.join("tests", "samples", rtl))

    out = tmpdir.join("out.jed")
    cfg = os.path.join("tests", "samples", "device_reg.yaml")
    regal.pnr(str(netlist), cfg, str(out))

    with open(os.path.join("tests", "samples", jedec), "r") as f:
        assert f.read() == out.read()
