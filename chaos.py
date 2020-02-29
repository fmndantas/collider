from collisor import Disk, System

if __name__ == '__main__':
    disks = [Disk(radius=0.005) for _ in range(300)]
    print('created disks')
    system = System(disks, width=700, height=700)
    print('created system')
    system.simulate(10000, 50)
