import pyglet, math, random
from pyglet import gl

ROTATION_SPEED =5# px/s^2
ACCELERATION = 50 # rad/s

def load_image(path):
    image = pyglet.image.load(path)
    image.anchor_x = image.width//2 # set an anchor to the center of the image
    image.anchor_y = image.height//2 #
    return image

image = load_image('PNG/playerShip1_blue.png') #  loading an image
asteroid_image = load_image('PNG/Meteors/meteorBrown_med3.png')

pressed_keys = set() # witch keys have been presssed
batch = pyglet.graphics.Batch()
objects =[]

def distance(a, b, wrap_size):
    """Distance in one direction (x or y)"""
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result

def overlaps(a, b):
    """Returns true iff two space objects overlap"""
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared

class SpaceObject:
    'features common for every object in space'
    radius = 40
    def __init__(self):
        self.x = window.width / 2
        self.y =window.height / 2
        self.rotation = 0
        self.x_speed = 0
        self.y_speed = 0
        self.sprite=pyglet.sprite.Sprite(image, batch=batch)


    def tick(self, dt):
        'move with an object'
        self.x += self.x_speed *dt
        self.y += self.y_speed *dt
        # return object to the window if it flies away
        self.x = self.x % window.width
        self.y = self.y % window.height

        # position of the sprite
        self.sprite.x = self.x
        self.sprite.y = self.y
        # correct rotation of the sprite
        self.sprite.rotation = 90 - math.degrees(self.rotation)

    def hit_by_spaceship(self, spaceship):
        'what to do in case of impact'
        return

    def delete(self):
        'delete a space object'
        if self in objects:
            objects.remove(self)
            self.sprite.delete()

class SpaceShip(SpaceObject):
    'features common for every spaceship'
    def __init__(self):
        'initialization'
        # set position to the center of the window
        super().__init__()
        self.sprite = pyglet.sprite.Sprite(image, batch=batch) # Sprite of the image


    def tick(self, dt):
        'movement of the spaceship'
        # rotate if left/right arrows are pressed
        if pyglet.window.key.LEFT in pressed_keys: # LEFT key pressed
            self.rotation = self.rotation + ROTATION_SPEED * dt # turn left
        if pyglet.window.key.RIGHT in pressed_keys: # RIGHT key pressed
            self.rotation = self.rotation - ROTATION_SPEED * dt # turn right

        # accelerate if up arrow is pressed
        if pyglet.window.key.UP in pressed_keys: #
            self.x_speed = self.x_speed + ACCELERATION*math.cos(self.rotation) # accelerate
            self.y_speed = self.y_speed + ACCELERATION*math.sin(self.rotation)
        super().tick(dt)

        for obj in objects:
            impact = overlaps(self, obj)
            if impact:
                obj.hit_by_spaceship(self)

class Asteroid(SpaceObject):
    'features common for every asteroid'
    def __init__(self):
        super().__init__()
        self.sprite = pyglet.sprite.Sprite(asteroid_image, batch=batch)
        # start at the edge of the Window
        if random.randrange(0, 2) == 0:
            # bottom edge
            self.x = random.randrange(0, window.width)
            self.y = 0
        else:
            #left edge
            self.x = 0
            self.y = random.randrange(0, window.height)

        self.x_speed = random.randrange(-100, 100)
        self.y_speed = random.randrange(-100, 100)

    def hit_by_spaceship(self, spaceship):
        spaceship.delete()

window = pyglet.window.Window()

# Create a spaceship and add it to the list of objects
spaceship = SpaceShip()
objects.append(spaceship)

# Create an asteroid
for i in range(3):
    asteroid = Asteroid()
    objects.append(asteroid)

def draw():
    'Draw all objects in the game'
    window.clear()

    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            # Remember the current state
            gl.glPushMatrix()
            # Move everything drawn from now on by (x_offset, y_offset, 0)
            gl.glTranslatef(x_offset, y_offset, 0)

            # Draw
            batch.draw()

            # Restore remembered state (this cancels the glTranslatef)
            gl.glPopMatrix()

def tick(dt):
    'move with objects'
    for obj in objects:
        obj.tick(dt)


def key_press(key, mod):
    'Add a key code to the set of pressed_keys'
    pressed_keys.add(key)

def key_release(key, mod):
    'Remove a key code from the set of pressed_keys'
    pressed_keys.discard(key)

pyglet.clock.schedule_interval(tick, 1/30) # interval volání fce tick()

#Register functions Pyglet should call on various events
window.push_handlers(
    on_draw=draw, # událost vykreslení
    on_key_press=key_press, # událost stisknutí klávesy
    on_key_release=key_release, # událost uvolnění klávesy
)

pyglet.app.run()
