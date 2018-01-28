module top (
    input a,
    input b,
    input c,
    output x,
    output y,
    output z
);

assign x =
  (~a & b) |
  (a & ~b)
;

assign y =
  (~a & ~b) |
  (a & b)
;

assign z =
  (~c) |
  (~b)
;

endmodule
