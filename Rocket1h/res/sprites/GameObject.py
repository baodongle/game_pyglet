import pyglet


def preload_image(image):
    img = pyglet.image.load('res/sprites/' + image)
    return img


class GameObject:
    def __init__(self, position_x, position_y, sprite=None):
        self.position_x = position_x
        self.position_y = position_y
        self.velocity_x = 0
        self.velocity_y = 0
        if sprite is not None:
            self.sprite = sprite
            self.sprite.x = self.position_x
            self.sprite.y = self.position_y
            self.width = self.sprite.width
            self.height = self.sprite.height

    def delete(self):
        self.sprite.delete()

    def draw(self):
        self.sprite.draw()

    def update(self):
        # self.position_x += self.velocity_x * dt
        # self.position_y += self.velocity_y * dt
        self.sprite.x = self.position_x
        self.sprite.y = self.position_y
