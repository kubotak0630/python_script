module reg
  (
   input wire clk,
   input wire reset_n
   )

  always @(posedge clk) begin

     if (!reset_n)
        r_120_nreg_ncs_hoge3 <= #(P_DLY) 32'h01020304;
     else
        r_120_nreg_ncs_hoge3 <= #(P_DLY) 0;


      if (reset_n) begin
        r_120_nreg_ncs_hoge1 <= #(P_DLY) 32'h0a0b0c0d;
     end
     else begin
        r_120_nreg_ncs_hoge1 <= #(P_DLY) 0;
     end

      if (reset_n) begin
        r_120_nreg_ncs_hoge2 <= #(P_DLY) 32'h1a1b1c1d;
     end
     else begin
        r_120_nreg_ncs_hoge2 <= #(P_DLY) 0;
     end

      if (reset_n) begin
        r_120_nreg_ncs_hoge0 <= #(P_DLY) 32'h2a2b2c2d;
     end
     else begin
        r_120_nreg_ncs_hoge0 <= #(P_DLY) 0;
     end
  end

endmodule
