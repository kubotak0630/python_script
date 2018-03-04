module tb_top();


   hoge u_hoge
     (
      .clk(clk),
      .reset(rest),
      .nreg_ncs_hoge0(nreg_ncs_hoge0  ),
      .nreg_ncs_hoge1(  nreg_ncs_hoge1),
      .hoge_out()

      );


   hoge1 u_hoge2
     (
      .clk(clk),
      .reset(rest),
      .nreg_ncs_hoge2(nreg_ncs_hoge2),
      .nreg_ncs_hoge3(nreg_ncs_hoge3),
      .hoge_out()

      );
   



endmodule
