# alright
# I need to be smarter about it this time
# but we can go robot by robot from the side of the person
# and evaluate the "cheapest" way to make the next robot down the line do a specific thing
# eg.
# I assume I have all prices for all movements of robot n-1, it's just a 5x5 matrix
# I want to evaluate the price of robot n to go from e.g. A to >
# so I calculate all possible sequences robot n-1 might need to input to go there
# based on the matrix I can calculate the cost for each of those moves
# I pick the smallest one and put it in the matrix

# I can pre-calculate these matrices before even reading in the input
# and then the last step is reading the input, generating only the numeric keypad routes I need and from that the prices

# the matrix structure
# A 2D 5x5 list for each directional keypad
# the first index is the start position, the second index is the end position
# in this order: ^ A < v >
# so from the keypad view the index is (i+3*j)-1
# the first matrix is full of 1s because a person inputs it
# we'll store the matrices in a list too to keep the robots organized
# our testcase will be part a

# let's get the parts from part a we reuse

# global constants
NUMERIC_KEYPAD = [["7","8","9"],["4","5","6"],["1","2","3"],["","0","A"]]
NUMERIC_VALIDATION = [[True,True,True],[True,True,True],[True,True,True],[False,True,True]]
DIRECTION_KEYPAD = [["","^","A"],["<","v",">"]]
DIRECTION_VALIDATION = [[False,True,True],[True,True,True]]

def get_character_position(grid,character):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == character:
                return [i,j]

DIRECTION_ARR = [[0,1],[1,0],[0,-1],[-1,0]]

def array_add(arr1,arr2):
    output = [0] * len(arr1)
    for i in range(len(arr1)):
        output[i] = arr1[i] + arr2[i]
    return output

def validate_sequence(validation_grid,start,sequence):
    if not validation_grid[start[0]][start[1]]:
        return False
    pos = start
    for character in sequence:
        if character == "<":
            direction = DIRECTION_ARR[2]
        elif character == ">":
            direction = DIRECTION_ARR[0]
        elif character == "^":
            direction = DIRECTION_ARR[3]
        elif character == "v":
            direction = DIRECTION_ARR[1]
        else:
            return True
        
        pos = array_add(pos,direction)
        if not validation_grid[pos[0]][pos[1]]:
            return False
    
def generate_candidate_sequences(start_pos,target_pos,validation_grid):
    vertical = start_pos[0] - target_pos[0]
    down = vertical < 0
    vertical = abs(vertical)
    horizontal = start_pos[1] - target_pos[1]
    left = horizontal > 0
    horizontal = abs(horizontal)

    vert_character = "v" if down else "^"
    horiz_character = "<" if left else ">"
    characters = [vert_character,horiz_character]
    length_sequence = vertical + horizontal
    
    sequences = []
    for i in range(2**length_sequence):
        combination = [int(num) for num in (bin(i)[2:])] # 0 is vertical, 1 is horizontal
        while len(combination) < length_sequence:
            combination = [0] + combination
        if sum(combination) != horizontal:
            continue
        combination_symbols = [characters[inx] for inx in combination] + ["A"]
        if validate_sequence(validation_grid,start_pos,combination_symbols):
            sequences.append(''.join(combination_symbols))
    return sequences

# I don't really want to mess with these methods so let's generate a function which translates a sequecne into a series of positions

def positions_from_string(string_sequence):
    output = []
    for character in string_sequence:
        n = ["^","A","<","v",">"].index(character)+1
        output.append([int(n/3),n%3])
    return output

num_dir_keypads = 26

matrices = [None]*num_dir_keypads

matrices[0] = [[1]*5 for i in range(5)] # our personal keypad

for n in range(1,num_dir_keypads):
    matrices[n] = [[1]*5 for i in range(5)]
    for i in range(5):
        for j in range(5):
            if i == j:
                # just press A again
                continue
            start_pos = [int((i+1)/3),(i+1)%3]
            target_pos = [int((j+1)/3),(j+1)%3]
            potential_sequences = generate_candidate_sequences(start_pos,target_pos,DIRECTION_VALIDATION)
            prices = [0]*len(potential_sequences)
            for k in range(len(potential_sequences)):
                potential_sequence = positions_from_string('A' + potential_sequences[k]) # we start from A always
                # now calculate the price based on matrix n-1
                for l in range(1,len(potential_sequence)):
                    subsequence_start = potential_sequence[l-1]
                    subsequence_start_index = (subsequence_start[0]*3+subsequence_start[1])-1
                    subsequence_end = potential_sequence[l]
                    subsequence_end_index = (subsequence_end[0]*3+subsequence_end[1])-1
                    prices[k] += matrices[n-1][subsequence_start_index][subsequence_end_index]
            # and keep the lowest one
            matrices[n][i][j] = min(prices)

# read inputs
door_codes = []

with open('21-input.txt', 'r') as file:
    for line in file:
        door_codes.append(line[:-1])

def robot_0_input(keycode):
    robot_pos = get_character_position(NUMERIC_KEYPAD,"A")
    sequences = []
    for character in keycode:
        robot_target = get_character_position(NUMERIC_KEYPAD,character)
        if all([robot_target[0] == robot_pos[0],robot_target[1] == robot_pos[1]]):
            sequences.append(["A"])
        else:
            sequences.append(generate_candidate_sequences(robot_pos,robot_target,NUMERIC_VALIDATION))

        robot_pos = robot_target
    return sequences

score = 0
for code in door_codes:
    subscore = 0
    robot_0_candidates = robot_0_input(code)
    for character_sequences in robot_0_candidates:
        prices = [0]*len(character_sequences)
        for k in range(len(character_sequences)):
            potential_sequence = positions_from_string('A' + character_sequences[k]) # we start from A always
            # now calculate the price based on the last matrix -1
            for l in range(1,len(potential_sequence)):
                subsequence_start = potential_sequence[l-1]
                subsequence_start_index = (subsequence_start[0]*3+subsequence_start[1])-1
                subsequence_end = potential_sequence[l]
                subsequence_end_index = (subsequence_end[0]*3+subsequence_end[1])-1
                prices[k] += matrices[-1][subsequence_start_index][subsequence_end_index]
        subscore += min(prices)
    score += subscore*int(code[:-1])

print(score)

