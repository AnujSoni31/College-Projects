import os
import music21 as m21 # music file manipulation - music representation
#pip install music21

KERN_DATASET_PATH = 'deutschl/test/'
SAVE_DIR = 'dataset'

ACCEPTABLE_DURATONS = [ 0.25, 0.5, 0.75, 1.0, 1.5, 2, 3, 4 ] # 1 note = 4 beats

'''
Representation:-
	pitch notation by number
	note hold by underscore
	rest by symbol 'r'
'''
def load_song_kern(dataset_path):
	songs = [] # to load all the songs

	# go through all the files to load them with music21
	for path, subdirs, files in os.walk(dataset_path):
		for file in files:
			# filter non-krn file
			if(file[-3:] == 'krn'):
				print(file)
				song = m21.converter.parse(os.path.join(path, file))
				songs.append(song)

	return songs

def has_acceptable_duration(song, acceptable_duration): #bool function
	for note in song.flat.notesAndRests: #flat changes song into list of notes and rests
		if note.duration.quarterLength not in acceptable_duration:
			return False
	return True # song has acceptable duration

def transpose(song): # transpose to Cmaj, Amin
	# get key from song
	parts = song.getElementsByClass(m21.stream.Part)
	measure_part0 = parts[0].getElementsByClass(m21.stream.Measure)
	key = measure_part0[0][4] # index 4 has the key stored

	# estimate key using Music21 if we don't have a key
	if not isinstance(key, m21.key.Key):
		key = song.analyze('key') # analyze() guesses key
	
	print(key)

	# get the interval for transposition (i.e. difference b/w current note and Cmaj or Amin)
	'''
	if note is maj convert to Cmaj
	else Amin
	'''
	if key.mode == 'major':
		interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch('C'))
	elif key.mode == 'minor':
		interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch('A'))

	# transpose song by calculated interval
	transposed_song = song.transpose(interval)

	return transposed_song

def encode_song(song, time_step=0.25): #0.25 -> 16th note
	# encode notes and rests to integer values
	# Example pitch = 60 and duration = 1.0 -> [60, '_', '_', '_'] 

	encoded_song = []
	for event in song.flat.notesAndRests:
		# handle note
		if isinstance(event, m21.note.Note):
			symbol = event.pitch.midi
		# handle rest (r)
		if isinstance(event, m21.note.Rest):
			symbol = 'r'

		# convert notes and rest into time series notation
		steps = int(event.duration.quarterLength / time_step)

		for step in range(steps):
			if step == 0: # if note
				encoded_song.append(symbol)
			else: # if rest
				encoded_song.append('_')
	
	# cast encoded song to string
	encoded_song = " ".join(map(str, encoded_song)) 
	return encoded_song

def preprocess(dataset_path):

	print('Loading Songs...')
	# load the songs
	songs = load_song_kern(dataset_path)
	print(f'Loaded {len(songs)} songs...')

	for index, song in enumerate(songs):
	# filter songs according to the duration
		if not has_acceptable_duration(song, ACCEPTABLE_DURATONS):
			continue # skip the song

	# transpose songs to Cmaj/Amin
	song = transpose(song)

	# encode songs with music time series representation
	encoded_song = encode_song(song)

	# save songs to text file
	save_path = os.path.join(SAVE_DIR, str(index))

	with open(save_path, 'w') as fp:
		fp.write(encoded_song)

if __name__ == '__main__':
	songs = load_song_kern(KERN_DATASET_PATH)
	print(f'Loaded {len(songs)} songs.')
	song = songs[0]
	
	preprocess(KERN_DATASET_PATH)
	transposed_song = transpose(song)
	
	song.show()
	transposed_song.show()