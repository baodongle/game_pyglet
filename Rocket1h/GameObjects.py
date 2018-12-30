import pyglet


def preload_image(image):
    img = pyglet.image.load('res/sprites/' + image)
    return img


def preload_media(media):
    vid = pyglet.media.load('res/media/' + media)
    return vid


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
        # self.sprite.x += self.velx * dt
        # self.sprite.y += self.vely * dt
        # self.posx += self.velx * dt
        # self.posy += self.vely * dt
        # self.posx = self.sprite.x
        # self.posy = self.sprite.y
        self.sprite.x = self.position_x
        self.sprite.y = self.position_y