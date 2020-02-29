from collisor import Disk, System

if __name__ == '__main__':
    r = 0.02
    d = 2 * r
    v = 0

    ball_A = Disk(rx=0.5, ry=0.2, radius=r, vx=v, vy=v)
    ball_B = Disk(rx=0.5 - d, ry=0.2, radius=r, vx=v, vy=v)
    ball_C = Disk(rx=0.5 + d, ry=0.2, radius=r, vx=v, vy=v)
    ball_D = Disk(rx=0.5, ry=0.2 + d, radius=r, vx=v, vy=v)

    ball_E = Disk(rx=1, ry=1, radius=r, vx=-2.4, vy=-4)

    balls = [ball_A, ball_B, ball_C, ball_D, ball_E]
    system = System(balls, width=800, height=800)
    system.simulate(10000, 60)
