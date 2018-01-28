module top (
    input a, b, c,
    output x, y, z
);

assign x = a ^ b;
assign y = ~x;
assign z = ~(c & b);

endmodule
