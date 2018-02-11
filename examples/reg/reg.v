module top (
    input Clk,
    input A,
    input B,

    output X,
    output reg Clk2
);

assign X = A ^ B;

always @(posedge Clk)
  Clk2 <= ~Clk2
;

endmodule
