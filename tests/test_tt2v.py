import pytest
import os
from regal.dump import tt2v

_samples = [
    ("tt0.csv", "v0.v"),
    ("tt1.csv", "v1.v"),
    ("and.csv", "and.v"),
    ("or.csv", "or.v"),
    ("xor.csv", "xor.v"),
    ("not.csv", "not.v"),
    ("nand.csv", "nand.v"),
]

@pytest.mark.parametrize("csv,output", _samples)
def test_tt2v(csv, output, tmpdir):
    out = tmpdir.join("out.v")
    tt2v(os.path.join("tests", "samples", csv), str(out))
    with open(os.path.join("tests", "samples", output), "r") as f:
        assert out.read() == f.read()
