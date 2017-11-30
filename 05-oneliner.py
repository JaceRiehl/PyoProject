from pyo import *

s = Server().boot()

t=Degrade(FM(Choice([50]*9+[75,99],9,RandInt(3,.2,2,4)),[.25,.33,.5,.75],Sine(.03,0,4,4),TrigEnv(Metro(.1,6).play(),CosTable([(0,0),(99,1),(500,.3),(8191,0)]),.3)),4,Sine(.05,0,.06,.1)).out()

s.gui(locals())
