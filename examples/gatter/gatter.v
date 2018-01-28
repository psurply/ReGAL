module top (
    input a, b, c, d, e, f, g, h, i, j,
    output w, x, y, z
);

assign w = a & b & c;
assign x = !(d & e);
assign y = f | g;
assign z = (h & i) | (j);

endmodule
