from pyo import *

chord_x = [48, 55, 64, 70]
freq_x = midiToHz(chord_x)

s = Server().boot()

env = CosTable([(0,0),(300,1),(1000,.3),(8191,0)])
seq = Seq(time=.2, seq=[2,1,2,2,2,1,2,2,2,2,1,2,1,2,2,2,1,2,2,1,2], poly=1).play()
amp = TrigEnv(seq, table=env, dur=.25, mul=.2)
a = SineLoop(freq=freq_x, feedback=0.09, mul=amp).out()

s.gui(locals())
