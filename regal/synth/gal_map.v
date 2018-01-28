module \$_NOT_ (A, Y);

parameter TABLE = 0;
parameter DEPTH = 0;

input A;
output Y;


generate
    GAL_XOR _TECHMAP_REPLACE_ (
        .A (A),
        .Y (Y)
    );
endgenerate

endmodule


module \$sop (A, Y);

parameter WIDTH = 0;
parameter TABLE = 0;
parameter DEPTH = 0;

parameter GAL_SOP_WIDTH = 8;

input [WIDTH-1:0] A;
output Y;

wire [GAL_SOP_WIDTH-1:0] I;
assign I[GAL_SOP_WIDTH-1:WIDTH] = 0;
assign I[WIDTH-1:0] = A;

generate
    GAL_SOP #(.TABLE(TABLE), .WIDTH(WIDTH), .DEPTH(DEPTH))
    _TECHMAP_REPLACE_ (
        .I0 (I[0]), .I1 (I[1]), .I2 (I[2]), .I3 (I[3]),
        .I4 (I[4]), .I5 (I[5]), .I6 (I[6]), .I7 (I[7]),
        .O (Y)
    );
endgenerate

endmodule

module \$_DFF_P_ (C, D, Q);

input C;
input D;
output Q;


generate
    GAL_DFF _TECHMAP_REPLACE_ (
        .C (C),
        .D (D),
        .Q (Q)
    );
endgenerate

endmodule
