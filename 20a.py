track = []

with open('20-input.txt', 'r') as file:
    for line in file:
        row = []
        for character in line:
            if character != "\n":
                row.append(character)
        track.append(row)

def print_grid(grid):
    for line in grid:
        ln = ""
        for character in line:
            ln += character
            if len(character) < 2:
                ln += " "
        print(ln)

def get_start_position(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                return [i,j]
            
def get_num_position(grid,number):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == str(number):
                return [i,j]


def array_add(arr1,arr2):
    output = [0] * len(arr1)
    for i in range(len(arr1)):
        output[i] = arr1[i] + arr2[i]
    return output

# print_grid(track)
start_pos = get_start_position(track)
pos = start_pos

# first get the normal time in ps which it takes to get to a certain position along the track.

DIRECTION_ARR = [[0,1],[1,0],[0,-1],[-1,0]]
finished = False

track[pos[0]][pos[1]] = "0"
n = 0

while not finished:
    n += 1
    for direction in DIRECTION_ARR:
        test_pos = array_add(pos,direction)
        if track[test_pos[0]][test_pos[1]] in [".","E"]:
            break
    if track[test_pos[0]][test_pos[1]] == "E":
        finished = True
    pos = test_pos
    track[pos[0]][pos[1]] = str(n)

# print()
# print_grid(track)

cheats = []
for i in range(n-1):
    pos = get_num_position(track,i)
    for direction in DIRECTION_ARR:
        test_pos = array_add(array_add(pos,direction),direction)
        if not all([0 <= test_pos[0] <= len(track), 0 <= test_pos[1] <= len(track[0])]):
            continue
        try:
            value = track[test_pos[0]][test_pos[1]]
            value = int(value)
            if value > i+2:
                savings = value-i-2
                cheats.append(savings)
        except:
            continue

cheats.sort()
# print(cheats)

good_cheat_amount = 0
for number in set(cheats):
    if number >= 100:
        good_cheat_amount += cheats.count(number)
#     print(f"saving of {number} ps appears {cheats.count(number)} times")

print(good_cheat_amount)