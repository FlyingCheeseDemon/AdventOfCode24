connections = []

with open('23-input.txt', 'r') as file:
    for line in file:
        connections.append(line[:-1].split("-"))

# we're looking for 3-loops in a graph when given all the edges
# unfortunately I don't know much about graphs theory in this regard
# tactic:
# let's create a dictionary. the keys are the computers, the values are the computers they have edges to.
# this will make it very efficient to look up connections

computer_dict = {}
for connection in connections:
    for i in range(2):
        computer = connection[i]
        if computer not in computer_dict.keys():
            computer_dict[computer] = [connection[(i+1)%2]]
        
        for connection_2 in connections:
            for j in range(2):
                if computer == connection_2[j] and connection_2[(j+1)%2] not in computer_dict[computer]:
                    computer_dict[computer].append(connection_2[(j+1)%2])

found_loops = []
for computer in computer_dict.keys():
    if computer[0] == 't': # we only care about loops which start at computers with t in it
        for first_connection in computer_dict[computer]:
            for second_connection in computer_dict[first_connection]:
                if computer in computer_dict[second_connection]:
                    if not set([computer, first_connection, second_connection]) in found_loops: # sets since we don't care about order
                        found_loops.append(set([computer, first_connection, second_connection]))

print(found_loops)
print(len(found_loops))