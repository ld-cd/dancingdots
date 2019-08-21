import pyglet, time, argparse

import render, dot, configuration

parse = argparse.ArgumentParser()
parse.add_argument("configfile")
args = parse.parse_args()

config = configuration.read_config(configuration.open_config(args.configfile))
dots = configuration.generate_dots(config)
configuration.generate_tracks(config)

conf = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(width=config['window']['width'], height=config['window']['height'], config=conf)
pyglet.gl.glClearColor(*config['window']['bgcolor'], 1)

start_time = time.perf_counter()

def update(dt):
    pass

pyglet.clock.schedule_interval(update, 1/240)

@window.event
def on_draw():
    window.clear()
    render.render_all(dot_list = dots, start = start_time)

pyglet.app.run()