map = []

with open('6-input.txt', 'r') as file:
    for line in file:
        map.append(list(line[:-1])) # remove that newline, we need the map to end

class guard:

    def __init__(self,position,direction,map):
        self.position = position
        self.direction = direction
        self.map = map
        self.map[self.position[0]][self.position[1]] = 'X' # remove her from the map, so she doesn't run into her own past
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
                return map[look_onto[0]][look_onto[1]]
            except IndexError:
                return " " # means out of bounds too
            
    def move(self):
        self.map[self.position[0]][self.position[1]] = 'X'
        self.position = [self.position[0] + self.direction[0],self.position[1] + self.direction[1]]
        if self.map[self.position[0]][self.position[1]] == '.':
            self.steps_taken += 1

direction_dic = {
    "<": [0,-1],
    "^": [-1,0],
    ">": [0,1],
    "v": [1,0]
}

for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] in direction_dic.keys():
            # found her!
            position = [i,j]
            direction = direction_dic[map[i][j]]
            break
    if 'position' in locals():
        break

gisela = guard(position,direction,map)

while True:
    field = gisela.check_field_ahead()
    if field == "#":
        gisela.turn()
    elif field in [".","X"]:
        gisela.move()
    elif field == " ":
        print(gisela.steps_taken)
        break
