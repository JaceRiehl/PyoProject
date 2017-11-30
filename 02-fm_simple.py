from pyo import *

s = Server().boot()

fcar = 250
rat = 1.
fmod = fcar * rat
ind = LFO(freq=1, type=1, mul=.5, add=.5)
mod = Sine(freq=fmod, mul=fmod*ind*50)
car = Sine(freq=fcar+mod, mul=ind*0.3).out()

s.gui(locals())