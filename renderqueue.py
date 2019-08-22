class RenderQueue:
    def __init__(self, window):
        self.window = window
        self.queue = []

    def render(self):
        if self.queue:
            self.queue[0]()
    
    def next(self):
        self.queue = self.queue[1:]
    
    def add(self, source):
        self.queue.append(source)
    
    def clear(self):
        self.queue = []