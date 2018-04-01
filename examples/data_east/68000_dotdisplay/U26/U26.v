module top (
    input UDS,
    input LDS,
    input AS,
    input A21,
    input A4,
    input A22,
    input RW,
    input A3,
    input DTACK,
    input NC,
    output RAMWHI,
    output RAMWLO,
    output ROMLO,
    output BOUT,
    output RAMEN,
    output VPA,
    output ROMHI,
    output BIN
);

assign RAMWHI =
  (DTACK) |
  (RW) |
  (~A22) |
  (A21) |
  (UDS)
;

assign RAMWLO =
  (DTACK) |
  (RW) |
  (~A22) |
  (A21) |
  (LDS)
;

assign ROMLO =
  (~RW) |
  (A22) |
  (LDS)
;

assign BOUT =
  (A3) |
  (RW) |
  (~A22) |
  (~A4) |
  (~A21) |
  (AS)
;

assign RAMEN =
  (~A22) |
  (A21) |
  (AS)
;

assign VPA =
  (~A3) |
  (~A22) |
  (~A21) |
  (AS)
;

assign ROMHI =
  (~RW) |
  (A22) |
  (UDS)
;

assign BIN =
  (A3) |
  (~RW) |
  (~A22) |
  (~A4) |
  (~A21) |
  (AS)
;

endmodule
