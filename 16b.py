import copy

maze = []
maze_scores = []
print_mazes = False

with open('16-input.txt', 'r') as file:
    for line in file:
        row = []
        score_row = []
        for character in line:
            if character != "\n":
                row.append(character)
                score_row.append([-1,-1,-1,-1,False]) # score for each direction of arrival + active search site + step count
        maze.append(row)
        maze_scores.append(score_row)



def print_maze(maze):
    for line in maze:
        ln = ""
        for character in line:
            if len(character) < 2:
                character = character + " "
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

DIRECTION_STR = [">","v","<","^"]
DIRECTION_ARR = [[0,1],[1,0],[0,-1],[-1,0]]

if print_mazes:
    print_maze(maze)
start_pos = get_character_position(maze,"S")
end_pos = get_character_position(maze,"E")
direction = 0 # east [0,1]
maze_scores[start_pos[0]][start_pos[1]] = [0,-1,-1,-1,True]
maze[start_pos[0]][start_pos[1]] = "0"

found_shit = True
while found_shit:
    # keep going until no more paths are being followed
    found_shit = False
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            current_position = [i,j]
            current_situation = maze_scores[i][j]
            if maze_scores[i][j][4]:
                found_shit = True
                # active site to seach from
                for direction in range(4):
                    current_score = maze_scores[i][j][direction]
                    if current_score != -1:
                        for m in [-1,0,1]:
                            target_position = array_add(current_position,DIRECTION_ARR[(direction+m)%4])
                            if maze[target_position[0]][target_position[1]] != "#":
                                new_score = current_score + m*m*1000 + 1
                                old_score = maze_scores[target_position[0]][target_position[1]][(direction+m)%4]
                                if old_score == -1 or new_score < old_score:
                                    maze_scores[target_position[0]][target_position[1]][(direction+m)%4] = new_score
                                    if maze[target_position[0]][target_position[1]] != "E":
                                        maze_scores[target_position[0]][target_position[1]][4] = True
                maze_scores[i][j][4] = False


if print_mazes:
    print(maze_scores[end_pos[0]][end_pos[1]])
end_scores = maze_scores[end_pos[0]][end_pos[1]]
smallest_score = end_scores[0]
smallest_direction = 0
for i in range(1,4):
    if smallest_score == -1 or (end_scores[i] != -1 and end_scores[i] < smallest_score):
        smallest_score = end_scores[i]
        smallest_direction = i
print(smallest_score, smallest_direction)

def backtrack(maze_scores,position,last_direction):
    scores = maze_scores[position[0]][position[1]]
    maze[position[0]][position[1]] = "O"
    if position[0] == start_pos[0] and position[1] == start_pos[1]:
        return
    comparable_scores = copy.deepcopy(scores)
    for i in range(4):
        comparable_scores[i] = scores[(i+2)%4]
        if abs(i-last_direction) == 1 and scores[(i+2)%4] != -1:
            comparable_scores[i] += 1000

    minimum = 9e10 # big enough... not elegant but it works
    mask = [True]*4
    for i in range(4):
        if comparable_scores[i] == -1:
            mask[i] = False
        elif comparable_scores[i] < minimum:
            minimum = comparable_scores[i]
    for i in range(4):
        if comparable_scores[i] > minimum:
            mask[i] = False
    
    for i in range(4):
        if mask[i]:
            backtrack(maze_scores,array_add(position,DIRECTION_ARR[i]),i)

backtrack(maze_scores,end_pos,smallest_direction)

if print_mazes:
    print_maze(maze)

score = 0
for i in range(len(maze)):
    for j in range(len(maze[i])):
        if maze[i][j] == "O":
            score += 1
print(score)