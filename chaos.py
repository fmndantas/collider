from collider import Disk, System

if __name__ == '__main__':
    disks = [Disk(radius=0.025) for _ in range(50)]
    system = System(disks)
    system.simulate(1000, 100)
