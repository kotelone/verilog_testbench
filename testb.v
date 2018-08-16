`timescale 1 ns / 1 ns

module test_counter;

reg clk = 0;

//	Place the testbench logic here








always
  #10 clk = ~clk;


initial
begin
  #100000 $finish;
end

initial
begin
  $dumpfile("output.vcd");
  $dumpvars(0,test_counter);
end

endmodule