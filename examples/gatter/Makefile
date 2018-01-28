EXAMPLES = gatter.v
SYNTH_CONFIG = device.yaml

JED = $(EXAMPLES:.v=.jed)

REGAL = regal

all: $(JED)

%.jed: %.v
	$(REGAL) build -o $@ $(SYNTH_CONFIG) $<

.PHONY: all
