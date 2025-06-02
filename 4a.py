text = []
amount = 0
with open('4a-input.txt', 'r') as file:
    for line in file:
        text.append(line)

def check_mas(text,origin,direction,character):
    newpos = [origin[0]+direction[0],origin[1]+direction[1]]
    # we don't want to get out of bounds at the lower...
    if newpos[0] < 0 or newpos[1] < 0:
        return False
    # ... or upper end
    try:
        found_letter = text[newpos[0]][newpos[1]]
        if found_letter != character:
            return False

        if character == 'M':
            return check_mas(text,newpos,direction,'A')
        elif character == 'A':
            return check_mas(text,newpos,direction,'S')
        elif character == 'S':
            return True
    except IndexError:
        return False

for i in range(len(text)):
    for j in range(len(text[0])):
        # find a possible start
        current_char = text[i][j]
        if current_char == 'X':
            # see if it goes anywhere
            for l in [-1,0,1]:
                for m in [-1,0,1]:
                    if l == m == 0:
                        continue
                    direction = (l,m)
                    found_one = check_mas(text,(i,j),direction,'M')
                    if found_one:
                        print(f"position: {i,j}; direction: {direction}")
                        amount += 1

print(amount)
                    
