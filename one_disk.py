from collisor import Disk
from render import Render
from time import sleep
from random import random

if __name__ == '__main__':
    render = Render()
    disks = [Disk(radius=0.01, vx=random(), vy=random()) for _ in range(0, 1)]
    while True:
        step = 0.025
        render.update_and_clear()
        for i in range(0, len(disks)):
            disks[i].move(step)
            disks[i].draw(render)
        sleep(step)
