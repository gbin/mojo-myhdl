# MojoMyHDL

This is a project to get you started on the Mojo board using MyHDL & RHEA.

The snow example adds a led at the top of the 8 leds when you press a button and let the "snowflakes" fall.

It needs the requirements from requirements.txt + fix this problem on rhea : https://github.com/cfelton/rhea/issues/5

- compile.sh compiles and deploys on the mojo board
- mojo.py is a pure python implementation of the mojo-loader
- snow.py is a little demo that needs a button on pin 51

Change the py directly to switch from bitstream compilation to simulation.
