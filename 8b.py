antenna_dict = {}

with open('8-input.txt', 'r') as file:
    for m,line in enumerate(file):
        for n,field in enumerate(line[:-1]):
            if field != '.':
                if field in antenna_dict.keys():
                    antenna_dict[field].append([m,n])
                else:
                    antenna_dict[field] = [[m,n]]

antinode_list = []

def in_bounds(position_of_antinode):
    return (0 <= position_of_antinode[0] <= m) and (0 <= position_of_antinode[1] <= n)

for key in antenna_dict:
    list_of_antennas = antenna_dict[key]
    for i in range(len(list_of_antennas)):
        for j in range(len(list_of_antennas)):
            if i == j: # this time we only need each pair once
                continue
            # our antinode is a line m*x+b
            # through two points [x1,y1] and [x2,y2]
            # the difference of the two vectors gives me the thing to repeat
            basis = [0,0]
            for l in range(2):
                basis[l] = list_of_antennas[i][l]-list_of_antennas[j][l]
            # and add that difference to the first one of them until I'm out of bounds

            position_of_antinode = list_of_antennas[i][:]
            while in_bounds(position_of_antinode):
                if (position_of_antinode not in antinode_list):
                    antinode_list.append(position_of_antinode[:])
                for l in range(2):
                    position_of_antinode[l] = position_of_antinode[l]+basis[l]


print(len(antinode_list))
