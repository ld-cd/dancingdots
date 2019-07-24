import pyglet

def make_player(track):
    sources = [make_source(i) for i in track]
    player = pyglet.media.Player()
    for i in range(len(sources)):
        sg = pyglet.media.SourceGroup(sources[i].audio_format, None)
        sg.loop = True
        sg.queue(sources[i])
        make_scheduler(i, sg, track, player)
    return player

def make_scheduler(i, sg, track, player):
    phase = sum([track[k]['duration'] for k in range(len(track)) if k < i])
    period = sum([k['duration'] for k in track])
    def play_it(t):
        player.queue(sg)
        player.next_source()
    periodic = lambda t: pyglet.clock.schedule_interval(play_it, period)
    pyglet.clock.schedule_once(periodic, phase)
    if phase == 0:
        player.queue(sg)
    else:
        pyglet.clock.schedule_once(play_it, phase)

def make_source(snippet):
    if snippet['type'] == "file":
        return pyglet.media.load(snippet['filename'], streaming=False)