TARGETS = tst.v testb.v


all: output clean


output: 
	iverilog -o output.o $(TARGETS)
	vvp output.o

clean:
	rm output.o	