warehouse = []
robot_commands = []

with open('15-input.txt', 'r') as file:
    for line in file:
        if line[0] == '#':
            # map mode
            row = []
            for character in line:
                if character != "\n":
                    row.append(character)
            warehouse.append(row)
        else:
            # collect movements
            for character in line:
                if character != "\n":
                    robot_commands.append(character)

def get_robot_position(warehouse):
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "@":
                return [i,j]
            
def get_score(warehouse):
    score = 0
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "O":
                score += 100*i + j
    return score

def print_warehouse(warehouse):
    for line in warehouse:
        ln = ""
        for character in line:
            ln += character
        print(ln)

def array_add(arr1,arr2):
    output = [0] * len(arr1)
    for i in range(len(arr1)):
        output[i] = arr1[i] + arr2[i]
    return output

print_warehouse(warehouse)
print(robot_commands)

for command in robot_commands:
    # print(command)
    robot_pos = get_robot_position(warehouse)
    # print(robot_pos)
    if command == "<":
        direction = [0,-1]
    if command == ">":
        direction = [0,1]
    if command == "v":
        direction = [1,0]
    if command == "^":
        direction = [-1,0]
    target_pos = array_add(robot_pos,direction)
    target_object = warehouse[target_pos[0]][target_pos[1]]
    if target_object == ".":
        # just move
        warehouse[target_pos[0]][target_pos[1]] = "@"
        warehouse[robot_pos[0]][robot_pos[1]] = "."
    elif target_object == "#":
        # wall, do nothing
        pass
    elif target_object == "O":
        # now the fun begins
        next_free_spot = target_pos
        while warehouse[next_free_spot[0]][next_free_spot[1]] == "O":
            next_free_spot = array_add(next_free_spot,direction)
        if warehouse[next_free_spot[0]][next_free_spot[1]] == "#":
            pass
        elif warehouse[next_free_spot[0]][next_free_spot[1]] == ".":
            # move that shit
            warehouse[target_pos[0]][target_pos[1]] = "@"
            warehouse[robot_pos[0]][robot_pos[1]] = "."
            warehouse[next_free_spot[0]][next_free_spot[1]] = "O"
        else:
            print("How?")
    else:
        print("How did we end up here?")
    # print_warehouse(warehouse)
print(get_score(warehouse))