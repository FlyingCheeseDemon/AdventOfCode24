import copy

door_codes = []

with open('21-input.txt', 'r') as file:
    for line in file:
        door_codes.append(line[:-1])

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


def robot_12_input(robot_01_sequence):
    robot_pos = get_character_position(DIRECTION_KEYPAD,"A")
    sequences = []
    for character in robot_01_sequence:
        robot_target = get_character_position(DIRECTION_KEYPAD,character)
        if all([robot_target[0] == robot_pos[0],robot_target[1] == robot_pos[1]]):
            sequences.append(["A"])
        else:
            sequences.append(generate_candidate_sequences(robot_pos,robot_target,DIRECTION_VALIDATION))

        robot_pos = robot_target
    return sequences

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

def recursive_simplifier(input):
    if type(input) == str:
        return [input]
    else:
        answers = [""]
        for step in input:
            new_answers = []
            for option in step:
                lines = recursive_simplifier(option)
                for answer in answers:
                    for line in lines:
                        new_answers.append(answer + line)
            answers = new_answers
        return answers
                
score = 0
for code in door_codes:
    robot_0_candidates = robot_0_input(code)
    print(robot_0_candidates) 
    robot_1_candidates = []
    for i,character in enumerate(robot_0_candidates): # for i in range len(code) basically
        print(i)
        robot_1_candidates.append([])
        for j,subsequence in enumerate(character): # in case there were multiple options
            robot_1_candidates[i].append(robot_12_input(subsequence))

    print(robot_1_candidates)

    robot_2_candidates = []
    for i,character in enumerate(robot_1_candidates): # for i in range len(code) basically
        print(i)
        robot_2_candidates.append([])
        for j,subsequence in enumerate(character): # in case there were multiple options to enter the character
            robot_2_candidates[i].append([])
            for k,sub_sub_sequence in enumerate(subsequence): # for each input on the keypad for entering the sequence
                robot_2_candidates[i][j].append([])
                for h,sub3_sequence in enumerate(sub_sub_sequence): # in case there were multiple options
                    robot_2_candidates[i][j][k].append(robot_12_input(sub3_sequence)) # get all the ways to enter that sequence
    
    print(robot_2_candidates)
    # I only need the length of the best one
    # time for the loop of death
    # ok, no actually let's make it recursive
    simplified_sequences = recursive_simplifier(robot_2_candidates)
    # print(simplified_sequences)
    shortest = len(simplified_sequences[0])
    for sequence in simplified_sequences:
        if len(sequence) < shortest:
            shortest = len(sequence)
    print(shortest)
    subscore = shortest*int(code[:-1])
    score += subscore
    
print(score) # 164960