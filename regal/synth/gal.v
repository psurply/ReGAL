module GAL_XOR (
    input A,
    output Y
);

assign Y = A ^ 1;

endmodule

module GAL_SOP (
    input I0,
    input I1,
    input I2,
    input I3,
    input I4,
    input I5,
    input I6,
    input I7,

    output O
);

parameter WIDTH = 0;
parameter DEPTH = 0;
parameter TABLE = 0;

\$sop #(.WIDTH (WIDTH), .DEPTH(DEPTH), .TABLE(TABLE))
_sop (.A({I7, I6, I5, I4, I3, I2, I1, I0}), .Y(O));

endmodule
