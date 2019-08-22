import pyglet, time, argparse

import render, dot, configuration, renderqueue, scene

parse = argparse.ArgumentParser()
parse.add_argument("configfile")
args = parse.parse_args()

config = configuration.read_config(configuration.open_config(args.configfile))

conf = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(width=config['window']['width'], height=config['window']['height'], config=conf)
pyglet.gl.glClearColor(*config['window']['bgcolor'], 1)

rqueue = renderqueue.RenderQueue(window)
scene.display_scene(window, config, "fast", rqueue, True)

def update(dt):
    pass

pyglet.clock.schedule_interval(update, 1/240)

@window.event
def on_draw():
    window.clear()
    rqueue.render()

pyglet.app.run()