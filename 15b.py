warehouse = []
robot_commands = []

with open('15-input.txt', 'r') as file:
    for line in file:
        if line[0] == '#':
            # map mode
            row = []
            for character in line:
                if character == "#":
                    row.append("#")
                    row.append("#")
                elif character == "O":
                    row.append("[")
                    row.append("]")
                elif character == ".":
                    row.append(".")
                    row.append(".")
                elif character == "@":
                    row.append("@")
                    row.append(".")
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
            if warehouse[i][j] == "[":
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

# print_warehouse(warehouse)

def check_push_horizontally(warehouse,push_start,direction):
    test_next = array_add(array_add(push_start,direction),direction)
    value = warehouse[test_next[0]][test_next[1]]
    if value == "#":
        return False
    elif value == ".":
        return True
    elif value in ["[","]"]:
        return check_push_horizontally(warehouse,test_next,direction)
    
def execute_push_horizontally(warehouse,push_start,direction,carry_character):
    if carry_character == ".":
        return
    temp = warehouse[push_start[0]][push_start[1]]
    warehouse[push_start[0]][push_start[1]] = carry_character
    push_next = array_add(push_start,direction)
    execute_push_horizontally(warehouse,push_next,direction,temp)

def check_push_vertically(warehouse,push_start,direction):
    # returns the collected truth value of pushing and the coordinates of the objects to push
    test_next = array_add(push_start,direction)
    value = warehouse[test_next[0]][test_next[1]]
    if value == "#":
        return [False,[]]
    elif value == ".":
        return [True,[push_start]]
    elif value == "[":
        other_next = array_add(test_next,[0,1])
    elif value == "]":
        other_next = array_add(test_next,[0,-1])
    truth_1, to_push_1 = check_push_vertically(warehouse,test_next,direction)
    truth_2, to_push_2 =check_push_vertically(warehouse,other_next,direction)
    return [truth_1 and truth_2, to_push_1 + to_push_2 + [push_start]]

def execute_push_vertically(warehouse,push_positions,direction):
    direction = direction[0]
    # if direction is -1 we push upwards, meaning we have to process positions from low to high
    # if direction is 1 we push downwards and we process from high to low
    # print(push_positions)
    if direction == -1:
        start = 0
        end = len(warehouse)
    elif direction == 1:
        start = len(warehouse)
        end = 0
    else:
        print("Wie bin ich hier her gekommen")

    for row in range(start,end,-direction):
        for position in push_positions:
            if position[0] == row:
                if warehouse[row][position[1]] != ".": # we hit a duplicate, don't do it again
                    warehouse[row+direction][position[1]] = warehouse[row][position[1]]
                    warehouse[row][position[1]] = "."
                    

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
    elif target_object in ["[","]"]:
        # now the fun begins
        next_free_spot = target_pos
        if direction[0] == 0:
            # pushing horizontally
            if check_push_horizontally(warehouse,target_pos,direction):
                execute_push_horizontally(warehouse,target_pos,direction,"@")
                warehouse[robot_pos[0]][robot_pos[1]] = "."
        else:
            # pushing vertically
            if target_object == "[":
                other_next = array_add(target_pos,[0,1])
            elif target_object == "]":
                other_next = array_add(target_pos,[0,-1])
                
            truth_1, to_push_1 = check_push_vertically(warehouse,target_pos,direction)
            truth_2, to_push_2 = check_push_vertically(warehouse,other_next,direction)

            if truth_1 and truth_2:
                execute_push_vertically(warehouse,[robot_pos] + to_push_1 + to_push_2,direction)

    # print_warehouse(warehouse)
    # input()
print(get_score(warehouse))