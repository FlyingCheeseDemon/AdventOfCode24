map = []

with open('6-input.txt', 'r') as file:
    for line in file:
        map.append(list(line[:-1])) # remove that newline, we need the map to end

class guard:

    def __init__(self,position,direction,map):
        self.position = position[:]
        self.direction = direction[:]
        self.map = [x[:] for x in map] # notation for the copy by value...
        self.map[self.position[0]][self.position[1]] = '.'
        self.steps_taken = 1

    def __str__(self):
        text = f"{self.position} : {self.direction}"
        return text

    def turn(self):
        self.direction = [self.direction[1],-1*self.direction[0]]

    def check_field_ahead(self):
        look_onto = [self.position[0] + self.direction[0],self.position[1] + self.direction[1]]
        if look_onto[0] < 0 or look_onto[1] < 0:
            return " " # means out of bounds, were done
        else:
            try:
                return self.map[look_onto[0]][look_onto[1]]
            except IndexError:
                return " " # means out of bounds too
            
    def move(self):
        self.map[self.position[0]][self.position[1]] += direction_matrix[self.direction[0]+1][self.direction[1]+1] #keeps a history if she's been in this position in this direction before
        self.position = [self.position[0] + self.direction[0],self.position[1] + self.direction[1]]
        try:
            if self.map[self.position[0]][self.position[1]] == '.':
                self.steps_taken += 1
        except:
            pass

    def check_loop(self):
        traces = self.check_field_ahead()
        if direction_matrix[self.direction[0]+1][self.direction[1]+1] in traces:
            return True
        return False

direction_dic = {
    "<": [0,-1],
    "^": [-1,0],
    ">": [0,1],
    "v": [1,0]
}

direction_matrix = [['','^',''],['<','','>'],['','v','']]

for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] in direction_dic.keys():
            # found her!
            position = [i,j]
            direction = direction_dic[map[i][j]]
            break
    if 'position' in locals():
        break

gisela = guard(position,direction,map[:])

while True:
    field = gisela.check_field_ahead()
    if field == "#":
        gisela.turn()
    elif field == " ":
        gisela.move() # one last move to mark the exit position as stepped on
        break
    else:
        gisela.move()
    
loopcount = 0
for i in range(len(map)):
    for j in range(len(map[0])):
        # it's enough to try all the positions which have been visited in the first round. placing an obstacle anywhere else would have no effect
        if gisela.map[i][j] in [".","#"]:
            continue
        # her starting position is off limits
        if i == position[0] and j == position[1]:
            continue

        newmap = [x[:] for x in map]
        newmap[i][j] = "#"
        dieter = guard(position,direction,newmap)
        while True:
            field = dieter.check_field_ahead()
            if field == "#":
                dieter.turn()
            elif field == " ":
                break
            else:
                dieter.move()
                loop = dieter.check_loop()
                if loop:
                    loopcount += 1
                    break

print(loopcount)