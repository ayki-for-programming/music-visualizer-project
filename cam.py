class Camera:

    def __init__(self):
        self.shake = 0

    def update(self):
        self.shake *= 0.9
        