#!/bin/bash
rm -Rf xilinx
. /opt/Xilinx/14.7/ISE_DS/settings64.sh
./snow.py
./mojo.py -i xilinx/mojov3.bin -r -v -d /dev/ttyACM0
