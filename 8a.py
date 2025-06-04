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

for key in antenna_dict:
    list_of_antennas = antenna_dict[key]
    for i in range(len(list_of_antennas)):
        for j in range(len(list_of_antennas)):
            if i == j:
                continue
            position_of_antinode = [0,0]
            for l in range(2):
                position_of_antinode[l] = 2*list_of_antennas[i][l]-list_of_antennas[j][l]

            in_bounds = (0 <= position_of_antinode[0] <= m) and (0 <= position_of_antinode[1] <= n)
            if (position_of_antinode not in antinode_list) and in_bounds:
                antinode_list.append(position_of_antinode)

print(antinode_list)
print(len(antinode_list))
