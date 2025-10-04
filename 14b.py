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
# GRID_DIM = [11,7]
steps_passed = 0

def candidate(grid):
    avg_neighbors = 0
    sum_in_grid = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            value = grid[i][j]
            sum_in_grid += value
            neighbors = 0
            if value != 0:

                for a in range(3):
                    for b in range(3):
                        try:
                            neighbors += grid[i+a-1][j+b-1]
                        except IndexError:
                            pass
            neighbors *= value
            avg_neighbors += neighbors
            
    avg_neighbors /= sum_in_grid
    print(avg_neighbors)
    return avg_neighbors > 3

while True:
    steps_passed += 1
    grid_to_print = []
    for i in range(GRID_DIM[1]):
        grid_to_print.append([0]*GRID_DIM[0])
    for robot in robots:
        robot[0] += robot[2]
        robot[1] += robot[3]
        
        robot[0] %= GRID_DIM[0]
        robot[1] %= GRID_DIM[1]

        grid_to_print[robot[1]][robot[0]] += 1

    if candidate(grid_to_print):
        for i in range(GRID_DIM[1]):
            txt = ""
            for j in range(GRID_DIM[0]):
                txt += " " if grid_to_print[i][j] == 0 else "X"
            print(txt)
        print(steps_passed)
        exit = input()
        if exit != "":
            break



