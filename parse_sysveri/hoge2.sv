

Hello /* World4 */ World5

//define enum
typedef enum bit [2: 0] {
  HOGE_REG0 = 3'b001,
  HOGE_REG1 = 3'b010,
  HOGE_REG2 = 3'b011                       
} hoge_val;


 /*enum bit [2: 0] {VAL0 = 3'd0, VAL1 = 3'd1, VAL2 = 3'd2 } hoge2_val;*/


enum bit [2: 0] {VAL00 = 3'b000, VAL01 = 3'b001, VAL02 = 3'b010 } hoge3_val; //cc


typedef enum bit [7: 0] {
  TEMP_REG0 = 3'd1,
  TEMP_REG0 = 2,
  TEMP_REG0 = 8'h4                 
} temp_val;

reg temp1;

always @(posedge clk) begin
  
  temp1 <= 1'b1;
end

