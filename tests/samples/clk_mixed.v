module top (
    input Clk,
    input I0,
    input I1,

    output O0,
    output reg Clk2
);

assign O0 = I0 ^ I1;

always @(posedge Clk)
  Clk2 <=
  (~Clk2)
;

endmodule
