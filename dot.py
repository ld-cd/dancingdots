import time, pyglet, numpy as np, random

class Dot:
    def __init__(self, loc, radius, color, period, phase = 0, duty = 0.5, motile=False, window_size=[]):
        self.loc = loc
        self.radius = radius
        self.color = color
        self.period = period
        self.phase = phase
        self.duty = duty
        self.gen_vlist()
        self.motile = motile
        self.window_size = window_size
        self.last_on = False
    
    def gen_vlist(self):
        iters = int(4*np.pi*self.radius)
        s = np.sin(2*np.pi/iters)
        c = np.cos(2*np.pi/iters)
        l = self.loc.copy()
        d = [self.radius, 0]
        for i in range(iters + 1):
            l.extend(np.array(self.loc) + np.array(d))
            d = [d[0] * c - d[1] * s, d[1]*c + d[0] * s]
        self.vlist = pyglet.graphics.vertex_list(len(l) // 2, ('v2f', l))

    def is_on(self, start_time):
        t = time.perf_counter() + self.phase*self.period - start_time
        on = (t - self.period * ((t) // self.period))/self.period < self.duty
        if self.motile and on and not self.last_on:
            self.loc = [random.random() * self.window_size[0], random.random() * self.window_size[1]]
            self.gen_vlist()
        self.last_on = on
        return on
    
    def render(self):
        pyglet.gl.glColor3f(*self.color)
        self.vlist.draw(pyglet.gl.GL_TRIANGLE_FAN)