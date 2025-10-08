import copy

maze = []

with open('16-test2.txt', 'r') as file:
    for line in file:
        row = []
        for character in line:
            if character != "\n":
                row.append(character)
        maze.append(row)

def print_maze(maze):
    for line in maze:
        ln = ""
        for character in line:
            ln += character
        print(ln)

def get_character_position(maze, character):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == character:
                return [i,j]
            
def array_add(arr1,arr2):
    output = [0] * len(arr1)
    for i in range(len(arr1)):
        output[i] = arr1[i] + arr2[i]
    return output

direction_strings = [">","v","<","^"]
direction_arrays = [[0,1],[1,0],[0,-1],[-1,0]]

def move_one_step(maze,direction):
    direction_arr = direction_arrays[direction]
    maze = copy.deepcopy(maze)
    position = get_character_position(maze,"@")
    next_position = array_add(position,direction_arr)
    if maze[next_position[0]][next_position[1]] == "E":
        # print_maze(maze)
        return 0, maze
    if maze[next_position[0]][next_position[1]] == ".":
        maze[next_position[0]][next_position[1]] = "@"
        maze[position[0]][position[1]] = direction_strings[direction]
        # input()
        return 1, maze
    else:
        return 2, maze

def recursive_search(maze, direction, score):
    best_score_ahead = -1
    best_score_ccw = -1
    best_score_cw = -1
    # go ahead
    check, maze_ahead = move_one_step(maze,direction)
    if check == 0:
        print(score + 1)
        if score == 7035:
            pass
        return score + 1
    if check == 1:
        next_score = recursive_search(maze_ahead,direction,score+1)
        if next_score != -1:
            best_score_ahead = next_score
    
    # turn left
    check, maze_ccw = move_one_step(maze,(direction-1)%4)
    if check == 0:
        print(score + 1001)
        return score + 1001
    if check == 1:
        next_score = recursive_search(maze_ccw,(direction-1)%4,score+1001)
        if next_score != -1:
            best_score_ccw = next_score
    
    # turn right
    check, maze_cw = move_one_step(maze,(direction+1)%4)
    if check == 0:
        print(score + 1001)
        return score + 1001
    if check == 1:
        next_score = recursive_search(maze_cw,(direction+1)%4,score+1001)
        if next_score != -1:
            best_score_cw = next_score
    
    best_score = best_score_ahead
    if best_score == -1 or (best_score > best_score_ccw and best_score_ccw != -1):
        best_score = best_score_ccw
    if best_score == -1 or (best_score > best_score_cw and best_score_cw != -1):
        best_score = best_score_cw
    
    return best_score

print_maze(maze)
start_pos = get_character_position(maze,"S")
direction = 0 # east [0,1]
maze[start_pos[0]][start_pos[1]] = "@"
best_score = recursive_search(maze,direction,0)
print(best_score)