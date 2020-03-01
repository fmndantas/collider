from collider import Disk, System

if __name__ == '__main__':
    disks = [Disk(radius=0.05) for _ in range(10)]

    system = System(disks)
    system.simulate(100, 60)
