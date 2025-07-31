robots = []

with open('14-input.txt', 'r') as file:
    for line in file:
        _,position, velocity = line.split("=")
        pos1, pos2 = position.split(",")
        pos1 = int(pos1)
        pos2 = int(pos2[:-2])
        vel1, vel2 = velocity.split(",")
        vel1 = int(vel1)
        vel2 = int(vel2[:-1])
        robot = [pos1,pos2,vel1,vel2]
        robots.append(robot)

GRID_DIM = [101, 103]
STEPS = 100
quadrant_scores = [0,0,0,0]

for robot in robots:
    for i in range(STEPS):
        robot[0] += robot[2]
        robot[1] += robot[3]
    
    robot[0] %= GRID_DIM[0]
    robot[1] %= GRID_DIM[1]

    if robot[0] < GRID_DIM[0]/2-0.5 and robot[1] < GRID_DIM[1]/2-0.5:
        quadrant_scores[0] += 1
    elif robot[0] > GRID_DIM[0]/2-0.5 and robot[1] < GRID_DIM[1]/2-0.5:
        quadrant_scores[1] += 1
    elif robot[0] < GRID_DIM[0]/2-0.5 and robot[1] > GRID_DIM[1]/2-0.5:
        quadrant_scores[2] += 1
    elif robot[0] > GRID_DIM[0]/2-0.5 and robot[1] > GRID_DIM[1]/2-0.5:
        quadrant_scores[3] += 1

print(quadrant_scores)
solution = quadrant_scores[0]*quadrant_scores[1]*quadrant_scores[2]*quadrant_scores[3]
print(solution)