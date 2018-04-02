module top (
    input E,
    input BUF_FUL,
    input BRW,
    input BA15,
    input BA14,
    input BA13,
    input FIRQ,
    input BA1,
    input BA2,
    input BLD,
    output BUSY,
    output OSTAT,
    output BROM,
    output BRAM,
    output BIN,
    output DSP0,
    output DSP1,
    output BD7
);

assign BUSY =
  (~FIRQ) |
  (~BUF_FUL)
;

assign OSTAT =
  (BA2) |
  (BA1) |
  (~BA13) |
  (BA14) |
  (BA15) |
  (BRW) |
  (E)
;

assign BROM =
  (~BA15 & ~BA14) |
  (~BRW)
;

assign BRAM =
  (BA13) |
  (BA14) |
  (BA15) |
  (E)
;

assign BIN =
  (BA2) |
  (~BA1) |
  (~BA13) |
  (BA14) |
  (BA15) |
  (~BRW) |
  (E)
;

assign DSP0 =
  (~BA13) |
  (BA14) |
  (~BA15) |
  (BRW) |
  (E)
;

assign DSP1 =
  (~BA13) |
  (~BA14) |
  (BA15) |
  (BRW) |
  (E)
;

assign BD7 =
  (BLD) |
  (~BA2) |
  (~BA1) |
  (~BA13) |
  (BA14) |
  (BA15) |
  (~BRW) |
  (E)
;

endmodule
