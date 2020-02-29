import heapq
from render import Render
from time import sleep
from random import random


class Disk:
    def __init__(self, rx=None, ry=None, vx=None, vy=None, radius=0.1, mass=1, counter=0):
        self.rx = rx if rx is not None else random()
        self.ry = ry if ry is not None else random()
        self.vx = vx if vx is not None else random()
        self.vy = vy if vy is not None else random()
        self.radius = radius
        self.mass = mass
        self.counter = counter

    def draw(self, render):
        render.draw_disk(self.rx, self.ry, self.radius)

    def move(self, dt):
        self.rx += self.vx * dt
        self.ry += self.vy * dt

    def count(self):
        return self.counter

    def t_to_other_disk(self, other):
        if self == other:
            return float('inf')
        dx = other.rx - self.rx
        dy = other.ry - self.ry
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy
        dv_dr = dx * dvx + dy * dvy
        if dv_dr > 0:
            return float('inf')
        dv_dv = pow(dvx, 2) + pow(dvy, 2)
        dr_dr = pow(dx, 2) + pow(dy, 2)
        sigma = self.radius + other.radius
        d = pow(dv_dr, 2) - dv_dv * (dr_dr - pow(sigma, 2))
        if d < 0:
            return float('inf')
        if dv_dv == 0:
            return float('inf')
        return -(dv_dr + pow(d, 0.5)) / dv_dv

    def t_to_hor_wall(self):
        if self.vy == 0:
            return float('inf')
        dt_bottom = (1 - self.radius - self.ry) / self.vy
        dt_top = (self.radius - self.ry) / self.vy
        return max(dt_bottom, dt_top)

    def t_to_ver_wall(self):
        if self.vx == 0:
            return float('inf')
        dt_left = (1 - self.radius - self.rx) / self.vx
        dt_right = (self.radius - self.rx) / self.vx
        return max(dt_left, dt_right)

    def bounce_off(self, other):
        dx = other.rx - self.rx
        dy = other.ry - self.ry
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy
        dv_dr = dx * dvx + dy * dvy
        dist = self.radius + other.radius
        j = 2 * self.mass * other.mass * dv_dr / ((self.mass + other.mass) * dist)
        jx = j * dx / dist
        jy = j * dy / dist
        self.vx += jx / self.mass
        self.vy += jy / self.mass
        other.vx -= jx / other.mass
        other.vy -= jy / other.mass
        self.counter += 1
        other.counter += 1

    def bounce_off_hor_wall(self):
        self.vx *= -1
        self.counter += 1

    def bounce_off_ver_wall(self):
        self.vy *= -1
        self.counter += 1


class Event:
    def __init__(self, t, disk_a, disk_b):
        self.t = t
        self.disk_a = disk_a
        self.disk_b = disk_b
        self.count_a = self.disk_a.count() if disk_a is not None else -1
        self.count_b = self.disk_b.count() if disk_b is not None else -1
        self.status = self.set_status()

    def set_status(self):
        if self.disk_a is not None and self.disk_b is not None:
            status = "a->b"
        elif self.disk_a is None and self.disk_b is not None:
            status = "b->hor"
        elif self.disk_a is not None and self.disk_b is None:
            status = "a->ver"
        else:
            status = "render"
        return status

    def is_valid(self):
        if self.disk_a is not None and self.count_a != self.disk_a.count():
            return False
        if self.disk_b is not None and self.count_b != self.disk_b.count():
            return False
        return True

    def __lt__(self, other):
        return self.t < other.t

    def __repr__(self):
        return f"Event(t={self.t:.2g}, status={self.status})"


class System:
    def __init__(self, disks, width=500, height=500):
        self.events = []
        self.disks = disks
        self.render = Render(width=width, height=height)
        self.t = 0

    def redraw(self, limit, hz, sleep_time=0.02):
        self.render.update_and_clear()
        sleep(sleep_time)
        for disk in self.disks:
            disk.draw(self.render)
        if self.t < limit:
            heapq.heappush(self.events, Event(self.t + 1 / hz, None, None))

    def predict_collisions(self, disk, limit):
        if disk is None:
            return

        for other_disk in self.disks:
            dt = disk.t_to_other_disk(other_disk)
            if self.t + dt <= limit:
                heapq.heappush(self.events, Event(self.t + dt, disk, other_disk))

        dth = disk.t_to_hor_wall()
        if self.t + dth <= limit:
            heapq.heappush(self.events, Event(self.t + dth, disk, None))

        dtv = disk.t_to_ver_wall()
        if self.t + dtv <= limit:
            heapq.heappush(self.events, Event(self.t + dtv, None, disk))

    def simulate(self, limit, hz):
        for disk in self.disks:
            self.predict_collisions(disk, limit)
        heapq.heappush(self.events, Event(0, None, None))
        while len(self.events):
            event = heapq.heappop(self.events)

            if not event.is_valid():
                continue

            for disk in self.disks:
                disk.move(event.t - self.t)
            self.t = event.t

            a, b = event.disk_a, event.disk_b
            if a is not None and b is not None:
                a.bounce_off(b)
            elif a is not None and b is None:
                a.bounce_off_ver_wall()
            elif a is None and b is not None:
                b.bounce_off_hor_wall()
            else:
                self.redraw(limit, hz)

            self.predict_collisions(a, limit)
            self.predict_collisions(b, limit)
