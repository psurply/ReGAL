module top (
    input Clk,
    output reg Clk2,
    output reg Clk4,
    output reg Clk8
);

always @(posedge Clk)
  Clk2 <=
  (~Clk2)
;

always @(posedge Clk)
  Clk4 <=
  (~Clk2 & ~Clk4) |
  (Clk2 & Clk4)
;

always @(posedge Clk)
  Clk8 <=
  (Clk4 & Clk8) |
  (~Clk2 & ~Clk4 & ~Clk8) |
  (Clk2 & Clk8)
;

endmodule
