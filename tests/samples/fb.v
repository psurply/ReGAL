module top (
    input A,
    input B,
    output C,
    output D
);

assign C = (A & B);
assign D = ~C;

endmodule
