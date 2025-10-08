import copy

maze = []
maze_scores = []

with open('16-input.txt', 'r') as file:
    for line in file:
        row = []
        score_row = []
        for character in line:
            if character != "\n":
                row.append(character)
                score_row.append([-1,-1,-1,-1,False]) # score for each direction of arrival + active search site
        maze.append(row)
        maze_scores.append(score_row)


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

DIRECTION_STR = [">","v","<","^"]
DIRECTION_ARR = [[0,1],[1,0],[0,-1],[-1,0]]

print_maze(maze)
start_pos = get_character_position(maze,"S")
end_pos = get_character_position(maze,"E")
direction = 0 # east [0,1]
maze_scores[start_pos[0]][start_pos[1]] = [0,-1,-1,-1,True]

found_shit = True
while found_shit:
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
                                    maze_scores[target_position[0]][target_position[1]][4] = True
                maze_scores[i][j][4] = False


print(maze_scores[end_pos[0]][end_pos[1]])