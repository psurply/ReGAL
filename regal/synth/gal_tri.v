module GAL_TRI (
    input A,
    input OE,
    output Y
);

assign Y = OE ? A : 1'bz;

endmodule
