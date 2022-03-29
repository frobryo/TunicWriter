import eng_to_ipa as ipa
import svgwrite

def ipa_to_glyphs(word):
	outlist=[]
	x=0;
	while x<len(word):
		base = word[x]
		x+=1
		if base == "ˈ" or base == "ˌ":
			outlist.append(".")
			continue
		if x!=len(word):
			if is_vowel(base+word[x]):
				outlist.append(base+word[x])
				x+=1
				continue
		outlist.append(base)
	print(outlist)
	return(outlist)

def display_tunic(word,dwg):
	pos = 0;
	x=0;
	while x<len(word):
		pos += 1
		base = word[x]
		x+=1
		if base == ".":
			pos = pos - 1
			continue
		if is_vowel(base):
			glyphprint(base,pos,dwg)
			if x<len(word):
				next = word[x]
				if is_consonant(next):
					glyphprint(next,pos,dwg)
					circprint(pos,dwg)
					x+=1
			#printline(shift(groundline,pos*width))				
		elif is_consonant(base):
			glyphprint(base,pos,dwg)
			if x<len(word):
				next = word[x]
				if is_vowel(next):
					glyphprint(next,pos,dwg)
					x+=1
	dwg.save()

vowels = ["i","u","ɛ","ə","aɪ","ɪ","ɑ","oʊ","əɹ","eɪ","ɔɹ","ʊɹ","ɪɹ","æ","ɛɹ","aʊ","ɔ","ɒ","ʊ","ɔɪ"]

def is_vowel(ipastr):
	return ipastr in vowels

consonants = ["b","t","n","ɹ","r","l","p","s","j","ð","h","d","ʧ","θ","g","ŋ","k","ʤ","v","w","z","f","m","ʃ","ʒ"]

def is_consonant(ipastr):
	return ipastr in consonants

vowelsegments = [[1,3,4,5],[1,2,3,4],[3,4,5],[1,2],[2],[4,5],[1,2,4,5],[1,2,3,4,5],[2,3,4,5],[1],[1,2,3,5],[1,2,3,5],[1,3,5],[1,2,3],[3,5],[5],[1,3],[1,3],[3,4],[4]]

consonantsegments = [[2,6],[1,3,5],[1,4,6],[2,3,5],[2,3,5],[2,5],[3,5],[2,3,4,5],[1,2,5],[2,4,5,6],[2,5,6],[2,4,6],[1,5],[1,2,3,5],[3,5,6],[1,2,3,4,5,6],[2,3,6],[2,4],[1,2,6],[1,3],[1,2,5,6],[3,4,5],[4,6],[1,3,4,5,6],[1,2,3,4,6]]

vowellines = [[],[[0,0.18605,0.2907,0]],[[0.5814,0.18605,0.2907,0]],[[0,0.18605,0,0.48256],[0,0.62791,0,0.81395]],[[0,0.81395,0.2907,1]],[[0.2907,1,0.5814,0.81395]]]
consonantlines = [[],[[0,0.18605,0.2907,0.37209]],[[0.2907,0.48256,0.2907,0]],[[0.2907,0.37209,0.5814,0.18605]],[[0,0.81395,0.2907,0.62791]],[[0.2907,0.62791,0.2907,1]],[[0.2907,0.62791,0.5814,0.81395]]]
baseline = [0,0.48256,0.5814,0.48256]

def glyphprint(glyph,pos,dwg):
	#print("Position "+str(pos)+" "+glyph)
	xshift = pos*0.5814-0.5
	yshift = 0.0814
	if is_vowel(glyph):
		segs = vowelsegments[vowels.index(glyph)]
		for seg in segs: vowelsegprint(seg,xshift,yshift,dwg)
	if is_consonant(glyph):
		segs = consonantsegments[consonants.index(glyph)]
		for seg in segs: consonantsegprint(seg,xshift,yshift,dwg)
	dwg.add(dwg.line(((baseline[0]+xshift)*height,(baseline[1]+yshift)*height),((baseline[2]+xshift)*height,(baseline[3]+yshift)*height), stroke=svgwrite.rgb(0,0,0,'%'), stroke_width=weight))

def vowelsegprint(seg,xshift,yshift,dwg):
	for line in vowellines[seg]:
		dwg.add(dwg.line(((line[0]+xshift)*height, (line[1]+yshift)*height), ((line[2]+xshift)*height,(line[3]+yshift)*height), stroke=svgwrite.rgb(0, 0, 0, '%'),stroke_width=weight))

def consonantsegprint(seg,xshift,yshift,dwg):
	for line in consonantlines[seg]:
		dwg.add(dwg.line(((line[0]+xshift)*height, (line[1]+yshift)*height), ((line[2]+xshift)*height,(line[3]+yshift)*height), stroke=svgwrite.rgb(0, 0, 0, '%'),stroke_width=weight))

def circprint(pos,dwg):
	xshift = pos*0.5814-0.5
	yshift = 0.0814
	dwg.add(dwg.circle(((0.2907+xshift)*height,(1.1+yshift)*height),0.1*height,stroke=svgwrite.rgb(0,0,0,'%'),stroke_width=weight,fill="none"))

height = int(input("Desired text height in pixels: "))
weight = int(input("Desired line weight in pixels: "))
filename = input("Output filename: ")
testword = input("Enter a word to write: ")

tunicout = svgwrite.Drawing(filename)

if ipa.convert(testword)==testword+"*":
	print("Word not found in dictionary")
else: display_tunic(ipa_to_glyphs(ipa.convert(testword)),tunicout)



