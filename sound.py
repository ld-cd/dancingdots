import pyglet, pydub, simpleaudio

def make_player(track):
    sounds = sum([make_source(i) for i in track])
    return lambda t: simpleaudio.play_buffer(sounds.raw_data, sounds.channels, sounds.sample_width, sounds.frame_rate)

def make_source(snippet):
    if snippet['type'] == "file":
        audio = pydub.AudioSegment.from_file(snippet['filename'])
    audio = audio*((1000*snippet["duration"])//len(audio)) + audio[:(snippet["duration"]*1000)%len(audio)]
    return audio