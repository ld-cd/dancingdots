import pyglet, time

import configuration, render

def make_text(text, window):
    return pyglet.text.Label(text, font_name='Roboto', font_size=36, x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')

def scene_pre(window, config, scene, first):
    def scenemaker():
        if config['window']['blind']:
            if first:
                make_text("A", window).draw()
            else:
                make_text("B", window).draw()
        else:
            make_text(scene, window).draw()
    return scenemaker

def scene_actual(window, config, scene, first):
    start_time = time.perf_counter()
    dots = configuration.generate_dots(config, scene)
    
    def scenemaker():
        render.render_all(dot_list = dots, start = start_time)
    return scenemaker

def display_scene(window, config, scene, rqueue, first):
    rqueue.clear()
    rqueue.add(scene_pre(window, config, scene, first))
    rqueue.add(scene_actual(window, config, scene, first))
    track = configuration.generate_tracks(config, scene)[0]
    pyglet.clock.schedule_once(lambda t: rqueue.next(),  2)
    pyglet.clock.schedule_once(track, 2)