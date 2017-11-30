from pyo import *

s = Server().boot()

fcar = 250
rat = 0.499
fmod = fcar * rat
ind = LFO(freq=[2,3,5,7], type=1, mul=.5, add=.5)
mod = Sine(freq=fmod, mul=fmod*ind*10)
car = Sine(freq=fcar+mod, mul=ind*0.3).out()

s.gui(locals())

TrigBurst
