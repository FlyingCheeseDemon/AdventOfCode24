map = []

with open('10-input.txt', 'r') as file:
    for line in file:
        line = [int(n) for n in line[:-1]]
        map.append(line)

sum = 0
directions = [-1,0]

# stealing this from day 6
def add_lists(lst1,lst2):
    return [lst1[0] + lst2[0],lst1[1] + lst2[1]]

def check_field_ahead(position,direction,map):
    look_onto = add_lists(position,direction)
    if look_onto[0] < 0 or look_onto[1] < 0:
        return -1 # means out of bounds, were done
    else:
        try:
            return int(map[look_onto[0]][look_onto[1]])
        except IndexError:
            return -1 # means out of bounds too

def scan(position,map,found_nines,current_number,score):
    
    directions = [[1,0],[-1,0],[0,1],[0,-1]]
    for direction in directions:
        seeing = check_field_ahead(position,direction,map)
        if seeing == current_number + 1:
            if current_number + 1 == 9:
                if add_lists(position,direction) not in found_nines:
                    score += 1
                    found_nines.append(add_lists(position,direction))
            else:
                score,found_nines = scan(add_lists(position,direction),map,found_nines,current_number+1,score)

    return score,found_nines


for i in range(len(map)):
    for j in range(len(map)):
        if map[i][j] == 0:
            # trailhead found, let's find it's score
            score = 0
            found_nines = [] # because we cannot double count 9s we find on different paths

            score,_ = scan([i,j],map,found_nines,0,0)
            sum += score

print(sum)