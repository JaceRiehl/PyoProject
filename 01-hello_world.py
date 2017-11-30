from pyo import *

s = Server().boot()

a = Sine(freq=1000, mul=0.3).out()

s.gui(locals())
