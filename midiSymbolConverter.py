import time
import mido
import itertools
from itertools import product

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
allRhythms = {'.':[0.5],'I' : [1.0], ':' : [0.5, 0.5], 'v' : [-0.5,0.5], ' V' : [-0.5,0.5], 'X': [0.5,1.0], 'x': [0.5,1.0], '>' : [1.0,0.5], '<' : [-0.5,1.0], 'w' : [-0.5,-0.5,0.5], 'W' : [-0.5,-0.5,0.5], '+' : [-0.5,0.5,0.5], 'i' : [0.5,0.5,0.5], '-' : [1.5]};

inputs = ['.','I',':','v','V','W','x','X','>','<','w','+','i','~','(',')'];


def pitchclass(chord):
    #takes a list of pitches numbers and prints note names
    pc = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']
    result = []
    for n in range (len(chord)):
        result.append (pc[chord[n] % 12])
    return result

def pitch_delta (pitches):
    result = []
    for n in range(len(pitches)):
        result.append((pitches[n] - pitches[0]))
    return result

def delta_x (pitches):
    result = []
    for n in range(len(pitches)-1):
        result.append((pitches[n+1] - pitches[n]))
    return result

def transpose(chord, fundamental):
    result = []
    delta = pitch_delta(chord)
    for k in delta:
        result.append(k + fundamental)
    return result

port = mido.open_output()

def make_midi_chord(chord, fundamental, vel):
    result = []
    newchord = transpose(chord, fundamental)
    for k in newchord:
        result.append(mido.Message('note_on', note=k, velocity = vel))
        print("Midi Chord: ")
        print k;
    return result

def midi_chord_off(chord, fundamental): 
    result = []
    newchord = transpose(chord, fundamental)
    for k in newchord:
        result.append(mido.Message('note_off', note=k))
    return result

def play_midi_chord(out, chord, fund, dur, vel):
    mchord = make_midi_chord (chord, (fund), vel)
    for n in mchord:
        out.send(n)
    time.sleep(dur)
    mchord = midi_chord_off (chord, (fund))
    for n in mchord:
        out.send(n)
    print("Exiting play_midi_chord")



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

	print rhythmFinal;
	return rhythmFinal;


def enterChord():
	chords = list();
	chord = raw_input("Please enter a string of chord symbols: ")

	for k in chord.split(' '):
		chords.append(k.strip());
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
		velocityList.append(int(k.strip()));
		print velocityList;

	return velocityList;
	
def play():
	rhythmFinal = userRythm();
	chords = enterChord();
	basslines = enterTransposition();
	velocityList = enterVelocity();
	skip = 0;
	chordLen = len(chords); 
	bassLinesLen = len(basslines);
	velLen = len(velocityList);

	for k in range(len(rhythmFinal)):
		if(rhythmFinal[k] < 0):
			print("Rhythm");
			print rhythmFinal[k];
			play_midi_chord(port, allchords[chords[k%chordLen]], basslines[k%bassLinesLen], -1 * rhythmFinal[k], 0);
			skip += 1;
			
		else: 
			print rhythmFinal[k];
			play_midi_chord(port, allchords[chords[(k - skip)%len(chords)]], basslines[(k - skip) % bassLinesLen],
				rhythmFinal[k], velocityList[(k - skip) % velLen]);
			










play();