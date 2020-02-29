from collider import Disk, System

if __name__ == '__main__':
    disks = [Disk(radius=0.01) for _ in range(100)]
    system = System(disks, width=700, height=700)
    system.simulate(1000, 24)
