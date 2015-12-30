# MyHDL for the FPGA board Mojo v3

This is a project to get you started on the [Mojo v3 board](https://embeddedmicro.com/mojo-v3.html) using MyHDL & RHEA.

The snow example lights up a led at the top of the 8 leds when you press a button and let the "snowflakes" fall.

It needs the requirements from requirements.txt + [this fix on rhea](https://github.com/cfelton/rhea/issues/5). You need Xilinx ISE Design Suite to be able to compile the example.

- compile.sh compiles and deploys on the mojo board
- mojo.py is a pure python implementation of the mojo-loader
- snow.py is a little demo that needs a button on pin 51 with some tests + gtkwave visualization.

Change the py directly to switch from bitstream compilation to simulation.
