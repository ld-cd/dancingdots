import pyglet, pydub, simpleaudio

def make_player(track):
    sounds = sum([make_source(i) for i in track])
    simpleaudio.play_buffer(sounds.raw_data, sounds.channels, sounds.sample_width, sounds.frame_rate)
    pyglet.clock.schedule_interval(
        lambda t: simpleaudio.play_buffer(sounds.raw_data, num_channels = sounds.channels, bytes_per_sample = sounds.sample_width, sample_rate = sounds.frame_rate)
        , len(sounds)/1000)

def make_source(snippet):
    if snippet['type'] == "file":
        audio = pydub.AudioSegment.from_file(snippet['filename'])
    audio = audio*((1000*snippet["duration"])//len(audio)) + audio[:(snippet["duration"]*1000)%len(audio)]
    return audio