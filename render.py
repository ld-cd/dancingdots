import pyglet, numpy, time
import dot

def render_all(dot_list, start):
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    for i in dot_list:
        if i.is_on(start):
            i.render()