text = []
amount = 0
with open('4a-input.txt', 'r') as file:
    for line in file:
        text.append(line)

def check_x_mas(text,origin):

    MAS1 = get_letter_in_direction(text,origin,[-1,-1]) == 'M' and get_letter_in_direction(text,origin,[1,1]) == 'S'
    SAM1 = get_letter_in_direction(text,origin,[1,1]) == 'M' and get_letter_in_direction(text,origin,[-1,-1]) == 'S'
    MAS2 = get_letter_in_direction(text,origin,[1,-1]) == 'M' and get_letter_in_direction(text,origin,[-1,1]) == 'S'
    SAM2 = get_letter_in_direction(text,origin,[-1,1]) == 'M' and get_letter_in_direction(text,origin,[1,-1]) == 'S'

    return (MAS1 or SAM1) and (MAS2 or SAM2)


def get_letter_in_direction(text,origin,direction):
    newpos = [origin[0]+direction[0],origin[1]+direction[1]]
    if newpos[0] < 0 or newpos[1] < 0:
        return False
    try:
        char = text[newpos[0]][newpos[1]]
    except IndexError:
        return ' '
    return char

for i in range(len(text)):
    for j in range(len(text[0])):
        # find a possible start
        current_char = text[i][j]
        if current_char == 'A':
            found_one = check_x_mas(text,(i,j))
            if found_one:
                print(f"position: {i,j}")
                amount += 1

print(amount)
                    
