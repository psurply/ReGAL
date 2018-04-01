module top (
    input XA0,
    input A9,
    input A10,
    input A11,
    input A12,
    input A13,
    input A14,
    input A15,
    input E,
    input Q,
    input VMA,
    input RW,
    input MPIN,
    output ROMCS,
    output RAMCS,
    output IOPORT,
    output IOSTB,
    output SNDSTB
);

assign ROMCS =
  (~RW) |
  (~VMA) |
  (E) |
  (~A14 & ~A15)
;

assign RAMCS =
  (~VMA) |
  (E) |
  (A15) |
  (A14) |
  (A13) |
  (A9 & A10 & A11 & A12 & ~RW & ~MPIN)
;

assign IOPORT =
  (~VMA) |
  (E & ~Q) |
  (A15) |
  (A14) |
  (~A13) |
  (A12) |
  (A11) |
  (A10)
;

assign IOSTB =
  (~VMA) |
  (~Q & ~RW) |
  (E) |
  (A15) |
  (A14) |
  (~A13) |
  (A11)
;

assign SNDSTB =
  (RW) |
  (~VMA) |
  (Q) |
  (E) |
  (A15) |
  (A14) |
  (~A13) |
  (~A12) |
  (~A11) |
  (A10)
;

endmodule
