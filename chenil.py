#!/usr/bin/env python
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

from myhdl import always, always_comb, always_seq, Signal, ResetSignal, toVerilog, toVHDL, delay, traceSignals, Simulation, now, intbv, modbv, concat

from pprint import pprint
import rhea.build as build
from rhea.system import Clock
from rhea.build.boards import get_board

def ClkDriver(clk):
  halfPeriod = delay(10)
  @always(halfPeriod)
  def driveClk():
      clk.next = not clk
  return driveClk


def chenillar(led, clock, reset, button):
  maxcnt = int(clock.frequency/2)
  cnt = Signal(intbv(0,min=0,max=maxcnt)) # 1s
  state = Signal(modbv(1, min=0, max=256))

  @always_seq(clock.posedge, reset=reset)
  def rtl():
    if not reset:
      state.next = 1
      cnt.next = 0
    elif not button:
      state.next = state | 1
    elif cnt == maxcnt-1:  # 1s
      cnt.next = 0
      state.next = state << 1
    else:
      cnt.next = cnt + 1

  @always_comb
  def display():
    led.next = state
  return rtl, display

def run_mojo():
  brd = get_board('mojo')
  brd.add_port('button', pins=51, pullup=True)
  flow = brd.get_flow(top=chenillar)
  flow.run()
  info = flow.get_utilization()
  pprint(info)

def sim():
  clk = Clock(0, frequency=1000)
  rst = ResetSignal(0, active=1, async=False)
  led = Signal(intbv(0, min=0, max=255))
  inst = chenillar(led, clk, rst)
  sim = Simulation(inst, ClkDriver(clk))
  sim.run()

if __name__ == '__main__':
  run_mojo()
  #sim()

