module top (
    input E,
    input BA15,
    input BA14,
    input BA13,
    input BA12,
    input XA0,
    input BWA,
    input BA1,
    input XA5,
    input Q,
    output RAMWR,
    output RAMCS,
    output PORTIN,
    output CATCCS,
    output CORE,
    output BSE,
    output ROMCS,
    output ZA0
);

assign RAMWR =
  (BWA) |
  (BA13 & BA12) |
  (BA14) |
  (BA15) |
  (E)
;

assign RAMCS =
  (BA13 & BA12) |
  (BA14) |
  (BA15) |
  (E)
;

assign PORTIN =
  (~BA1) |
  (~BWA) |
  (~BA12) |
  (~BA13) |
  (BA14) |
  (BA15) |
  (E)
;

assign CATCCS =
  (BA1) |
  (~BA12) |
  (~BA13) |
  (BA14) |
  (BA15) |
  (E & Q)
;

assign CORE =
  (~BA14 & BA12) |
  (~BA14 & ~BA13) |
  (BA15)
;

assign BSE =
  (Q) |
  (~BA1) |
  (BWA) |
  (~BA12) |
  (~BA13) |
  (BA14) |
  (BA15)
;

assign ROMCS =
  (~BWA & Q) |
  (~BA15 & ~BA14) |
  (E & Q)
;

assign ZA0 =
  (BA14 & XA0) |
  (~BA15 & BA12 & XA0 & XA5) |
  (~BA15 & ~BA13 & BA12 & XA0) |
  (~BA15 & BA13 & XA0 & XA5) |
  (~BA15 & ~BA14 & BA12 & XA5) |
  (~BA15 & ~BA14 & ~BA13 & BA12) |
  (~BA15 & ~BA14 & BA13 & XA5) |
  (BA15 & BA14)
;

endmodule
