import logging
import yaml

from .probes import arduino_mega

_logger = logging.getLogger("regal_dump")
_logger.addHandler(logging.NullHandler())


def dump(dump_cfg):
    with open(dump_cfg, "r") as f:
        cfg = yaml.load(f)

    if cfg["probe"] == "arduino_mega":
        arduino_mega.dump(
            outfile=cfg["outfile"],
            device=cfg["device"],
            io=cfg["ios"]
        )
    else:
        _logger.error("Unknown probe: %s", cfg["probe"])
