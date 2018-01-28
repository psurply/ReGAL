module top (
    input A,
    input B,
    output C
);

assign C =
  (~B) |
  (~A)
;

endmodule
