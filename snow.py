#!/usr/bin/env python
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
from pprint import pprint
from subprocess import call
import argparse
import os
from random import randint

from myhdl import always, always_comb, always_seq, Signal, ResetSignal, toVerilog, toVHDL, delay, traceSignals, Simulation, now, intbv, modbv, concat, instance, StopSimulation
from rhea.system import Clock
from rhea.build.boards import get_board

def snow(led, clock, reset, button):
  """ A small demo module. button and reset are in reverse logic.
  This should insert a 'snowflake' on the top led and let it fall.
  """
  maxcnt = int(clock.frequency)
  cnt = Signal(intbv(0,min=0,max=maxcnt)) # 1s
  state = Signal(modbv(0)[8:])

  @always(clock.posedge)
  def rtl():
    if reset:
      cnt.next = 0
    elif not button:
      state.next = state | 1
    elif cnt == maxcnt-1:  # 1s
      if not reset:
        cnt.next = 0
        state.next = state << 1
    else:
      cnt.next = cnt + 1

  @always_comb
  def display():
    led.next = state
  return rtl, display

def compile_mojo():
  brd = get_board('mojo')
  brd.add_port('button', pins=51, pullup=True)  # you can plug directly a button there between pin51 and gnd.
  flow = brd.get_flow(top=snow)
  flow.run()
  info = flow.get_utilization()
  pprint(info)

def testbench():
  # First we instanciate the external world for this module
  # with something close enough to reality.
  clk = Clock(0, frequency=10)
  rst = ResetSignal(0, active=0, async=False)  # This is simulating the reset sig.
  led = Signal(intbv(0)[8:])       # the leds
  button = Signal(True)                       # the button


  def _bench():
    clkgen = clk.gen(5) # simulate the clock
    inst = snow(led, clk, rst, button)           # We hook it up to our implementation.

    @instance
    def stimulus():
      """ This simulates a button press after a while clocks. """

      # the mojo board auto-reset at the beginning
      yield clk.posedge
      rst.next = True
      yield clk.posedge
      rst.next = False
      for j in range(4):
        for i in range(randint(0, 50)):
          yield clk.posedge
        button.next = False
        yield clk.posedge
        button.next = True
      for i in range(100):
        yield clk.posedge
      raise StopSimulation
    return clkgen, stimulus, inst
  return _bench

def sim(visu = False):
  try:
    os.remove('_bench.vcd')
  except Exception as e:
    pass # just ignore, the file is probably not here.

  fsm = traceSignals(testbench())
  sim = Simulation(fsm)
  sim.run()
  if visu:
    call(['gtkwave', '_bench.vcd'])

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Snowflake demo for mojo v3.')
  parser.add_argument('--compile', dest='compile', action='store_const',
                      const=True, default=False,
                      help='Compile for the real hardware instead of a simulation, settings64.sh from ISE needs to be used to setup the environment first.')
  parser.add_argument('--visu', dest='visu', action='store_const',
                      const=True, default=False,
                      help='Start gtkwave to visualize the simulation.')
  args = parser.parse_args()
  if args.compile:
    compile_mojo()
  else:
    sim(args.visu)
