import time
import mido
import itertools
from itertools import product
from pyo import *
from random import uniform
import os

Cmadd2 = [48, 62, 63, 67]
Cm7 = [48, 55, 63, 70]
Cadd2 = [48, 62, 64, 67]
CM7 = [48, 55, 64, 71]
C7 = [48, 55, 64, 70]
C9 = [48, 55, 64, 70, 74]
CM9 = [48, 55, 64, 71, 74]
Cm7M13 = [48, 58, 63, 69, 74]
Cm11 = [48, 55, 65, 70, 75]
CmM7 = [48, 59, 63, 67, 74]
CmM7_2 = [48, 55, 63, 71, 74]
CM7s11 = [48, 55, 62, 66, 71]
Cm9_2 = [48, 55, 63, 70, 74]
Cm9 = [48, 58, 62, 63, 67]
CMaj9 = [48, 67, 59, 62, 64]
CM9_2 = [48, 59, 62, 64, 67]
C7s9 = [48, 55, 64, 70, 75]
CM7s5 = [48, 56, 59, 64]
Cm7b5 = [48, 58, 63, 66]
Cm7b5_2 = [48, 54, 63, 70]






allchords={'Cmadd2' : Cmadd2,'Cm7' : Cm7,'Cadd2' : Cadd2, 'CM7' : CM7, 'C7' : C7, 'C9' : C9, 
	'CM9' : CM9, 'Cm7M13' : Cm7M13, 'Cm11' : Cm11, 'CmM7' : CmM7, 'CmM7_2': CmM7_2, 'CM7s11' : CM7s11, 'Cm9_2' : Cm9_2, 'Cm9' : Cm9,
	'CMaj9' : CMaj9, 'CM9_2':CM9_2, 'C7s9':C7s9,'CM7s5':CM7s5,'Cm7b5':Cm7b5,'Cm7b5_2':Cm7b5_2, }
allRhythms = {'.':[1],'I' : [2], ':' : [1,1], 'v' : [-1,1], ' V' : [-1,1], 'X': [1,2], 'x': [1,2], '>' : [2,1], '<' : [-1,2], 'w' : [-1,-1,1], 'W' : [-1,-1,1], '+' : [-1,1,1], 'i' : [1,1,1], '-' : [3]};

inputs = ['.','I',':','v','V','W','x','X','>','<','w','+','i','~','(',')','-'];


def pitchclass(chord):
    #takes a list of pitches numbers and prints note names
    pc = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']
    result = []
    for n in range (len(chord)):
        result.append (pc[chord[n] % 12])
    return result

def pitch_delta (pitches):
    result = list()
    for n in range(len(pitches)):
        result.append((pitches[n] - pitches[0]))
    return result

def delta_x (pitches):
    result = []
    for n in range(len(pitches)-1):
        result.append((pitches[n+1] - pitches[n]))
    return result

def transpose(chords, fundamental):
    result = list();
    delta = list(); 
    funIndex = 0;
    for i in chords:
    	delta.append(pitch_delta(i))
    for k in delta:
    	for i in k:
    		result.append(i + fundamental[funIndex])
    	if(funIndex < len(fundamental)-1):
    		funIndex += 1
    	else:
    		funIndex = 0
    return result

# port = mido.open_output()

# def make_midi_chord(chord, fundamental, vel):
#     result = []
#     newchord = transpose(chord, fundamental)
#     for k in newchord:
#         result.append(mido.Message('note_on', note=k, velocity = vel))
#         print("Midi Chord: ")
#         print k;
#     return result

# def midi_chord_off(chord, fundamental): 
#     result = []
#     newchord = transpose(chord, fundamental)
#     for k in newchord:
#         result.append(mido.Message('note_off', note=k))
#     return result

# def play_midi_chord(out, chord, fund, dur, vel):
#     mchord = make_midi_chord (chord, (fund), vel)
#     for n in mchord:
#         out.send(n)
#     time.sleep(dur)
#     mchord = midi_chord_off (chord, (fund))
#     for n in mchord:
#         out.send(n)
#     print("Exiting play_midi_chord")



def userRythm():

	rhythm = list();
	rhythmAltered = list();
	rhythmFinal = list();

	rhy = raw_input("Please enter a string of rhythm symbols serperated by a space: ")

	for k in rhy.split(' '):
		k.strip();
		print k;
		if k in inputs:
			if k in allRhythms:
				rhythm.append(allRhythms[k]);
			else:
				rhythm.append(str(k));
		
		print rhythm;



		#collapse arrays
	for i in range(len(rhythm)):
		for j in range(len(rhythm[i])):
			rhythmAltered.append(rhythm[i][j])
	print rhythmAltered;


	j = 0;
	while(j < len(rhythmAltered)):
		 
		if(rhythmAltered[j] == '~'):
			if((rhythmAltered[j-1] > 0 and rhythmAltered[j+1] > 0)):
				rhythmFinal[-1] = rhythmAltered[j-1] + rhythmAltered[j+1]
			else: 
				rhythmFinal[-1] = rhythmAltered[j-1];
				rhythmFinal.append(rhythmAltered[j+1])

			j+=2;
			continue;
		if(rhythmAltered[j] == '('):
			k = j + 1;
			while(rhythmAltered[k] != ')'):
				if(rhythmAltered[k] > 0):
					rhythmFinal.append(rhythmAltered[k] * -1);
					k+=1;
				elif(rhythmAltered[k] < 0):
					rhythmFinal.append(rhythmAltered[k] * 1);
					k+=1;
			j = k + 1;
			#print("This is J: " + str(j));
			continue;

		if(rhythmAltered[j] > 0 or rhythmAltered[j] < 0):
			rhythmFinal.append(rhythmAltered[j]);
			j += 1;

	

	i = 0;
	while i < len(rhythmFinal):
		if(rhythmFinal[0] <= 0):
			del(rhythmFinal[0]);
			continue; 

		if(rhythmFinal[i] < 0 and i != 0):
			rhythmFinal[i-1] = -1 * rhythmFinal[i] + rhythmFinal[i-1];
			del(rhythmFinal[i]);
			continue;
		i += 1; 

	print rhythmFinal;
	return rhythmFinal;


def enterChord():
	chords = list();
	chord = raw_input("Please enter a string of chord symbols: ")

	for k in chord.split(' '):
		chords.append(allchords[k.strip()]);
		print chords;
	return chords;


def enterTransposition():
	basslines = list();
	bassline = raw_input("Please enter a string of bass lines: ")

	for k in bassline.split(' '):
		basslines.append(int(k.strip()));
		print basslines;
	return basslines;


def enterVelocity():
	velocityList = list();
	vel = raw_input("Please enter a string of velocities (between 0 and 127): ")

	for k in vel.split(' '):
		if(int(k.strip()) <= 127 and int(k.strip()) >= 0):
			velocityList.append(float(k.strip())/127);
		
	print velocityList;
	return velocityList;


	
def play():
	freq_x = list()
	rhythmFinal = userRythm();
	chords = enterChord();
	basslines = enterTransposition();
	velocityList = enterVelocity();
	# skip = 0;
	# chordLen = len(chords); 
	# bassLinesLen = len(basslines);
	# velLen = len(velocityList);
	transChords = list()
	
	transChords = transpose(chords, basslines)

	# path = input("Where do you want the recorded audio to be placed? ex. Desktop/FinalProject ")
	path = "/"
	# filename = input("What do you want your file name to be? ")
	for i in transChords:
		freq_x.append(midiToHz(i))


	# home = os.path.expanduser('~')
	s = Server().boot()
	# s.start()
	# s.recordOptions(dur=60, filename="./testFile.wav", fileformat=0, sampletype=0, quality=0.9)
	# met = Metro(time=.2, poly=1).play()
	
	# env = CosTable([(0,0),(300,1),(1000,.3),(8191,0)])
	env = CosTable([(0,0), (50,1), (250,.3), (8191,0)])
	seq = Seq(time=.2, seq=rhythmFinal, poly=1).play()
	amp = TrigEnv(seq, table=env, dur=.25, mul=velocityList)
	it = Iter(seq, choice=freq_x)
	lfo = Sine(freq=it, mul=amp)
	lfo.ctrl()
	a = SineLoop(freq=it, feedback=lfo, mul=amp)
	a.ctrl()
	# b = FastSine(freq=500*lfo, quality=1, mul=amp)
	# a = CrossFM(carrier=[250.5,250], ratio=[.2499,.2502], ind1=tr, ind2=tr, mul=.2).out(
	# a = FastSine(freq=it, quality=1, mul=0.02, add=1)
	# syn = FastSine(freq=500*a, quality=1, mul=0.4).out()
	sel = Selector([a,lfo])
	sel.ctrl(title="Input interpolator (0=SineLoop, 1=Sine)")
	sp = Spectrum(sel)
	n = PinkNoise(.5)
	f = BandSplit(n, num=6, min=250, max=4000, q=5, mul=sel).out()
	f.ctrl()
	rec = Record(f, filename="./someFile.wav",chnls=2, fileformat=0, sampletype=2)
	clean = Clean_objects(65, rec)
	clean.start()
	s.gui(locals())


	# for k in range(len(rhythmFinal)):
	# 	if(rhythmFinal[k] < 0):
	# 		print("Rhythm");
	# 		print rhythmFinal[k];
	# 		play_midi_chord(port, allchords[chords[k%chordLen]], basslines[k%bassLinesLen], -1 * rhythmFinal[k], 0);
	# 		skip += 1;
			
	# 	else: 
	# 		print rhythmFinal[k];
	# 		play_midi_chord(port, allchords[chords[(k - skip)%len(chords)]], basslines[(k - skip) % bassLinesLen],
	# 			rhythmFinal[k], velocityList[(k - skip) % velLen]);
			

play();