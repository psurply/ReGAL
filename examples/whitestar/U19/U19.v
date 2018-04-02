module top (
    input IN0,
    input PD7,
    input PD6,
    input PD5,
    input PD4,
    input PD3,
    input PD2,
    input PD1,
    input PD0,
    input SA1,
    output SD15,
    output SD14,
    output SD13,
    output SD12,
    output SD11,
    output SD10,
    output SD9,
    output SD8
);

assign SD15 =
  (PD7 & SA1) |
  (IN0)
;

assign SD14 =
  (PD6 & SA1) |
  (IN0)
;

assign SD13 =
  (PD5 & SA1) |
  (IN0)
;

assign SD12 =
  (PD4 & SA1) |
  (IN0)
;

assign SD11 =
  (PD3 & SA1) |
  (IN0)
;

assign SD10 =
  (PD2 & SA1) |
  (IN0)
;

assign SD9 =
  (PD1 & SA1) |
  (IN0)
;

assign SD8 =
  (PD0 & SA1) |
  (IN0)
;

endmodule
