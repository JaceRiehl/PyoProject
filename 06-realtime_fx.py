from pyo import *

s = Server().boot()

sf = SfPlayer(SNDS_PATH+"/transparent.aif", loop=True, mul=.5)

pva = PVAnal(sf, size=2048)
pvm = PVAmpMod(pva, basefreq=4, spread=0.5)
pvf = PVFreqMod(pvm, basefreq=8, spread=0.75, depth=0.05)
pvs = PVSynth(pvf).mix(2).out()

pvm.ctrl()
pvf.ctrl()

s.gui(locals())