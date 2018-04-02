EXAMPLES = U20.v
SYNTH_CONFIG = device.yaml

JED = $(EXAMPLES:.v=.jed)

REGAL = regal

all: $(JED)

%.jed: %.v
	$(REGAL) -v build -o $@ $(SYNTH_CONFIG) $<

.PHONY: all
