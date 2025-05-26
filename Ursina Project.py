from ursina import *

app = Ursina()

# Create ground
ground = Entity(model='cube', color=color.gray, scale=(8, 0.5, 8), y=-2)

# Create the jumping box
player = Entity(model='cube', color=color.orange, scale=(1,1,1), position=(0,0,0))

velocity_y = 0
gravity = -12
jump_strength = 6
on_ground = True

def update():
    global velocity_y, on_ground

    # Apply gravity
    velocity_y += gravity * time.dt
    player.y += velocity_y * time.dt

    # Ground collision
    if player.y <= 0:
        player.y = 0
        velocity_y = 0
        on_ground = True
    else:
        on_ground = False

def input(key):
    global velocity_y, on_ground
    if key == 'space' and on_ground:
        velocity_y = jump_strength
        on_ground = False

app.run()
