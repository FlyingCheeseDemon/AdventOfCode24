connections = []

with open('23-input.txt', 'r') as file:
    for line in file:
        connections.append(line[:-1].split("-"))

computer_dict = {}
longest_connection = 0
for connection in connections:
    for i in range(2):
        computer = connection[i]
        if computer not in computer_dict.keys():
            computer_dict[computer] = [connection[(i+1)%2]]
        
        for connection_2 in connections:
            for j in range(2):
                if computer == connection_2[j] and connection_2[(j+1)%2] not in computer_dict[computer]:
                    computer_dict[computer].append(connection_2[(j+1)%2])
                    if len(computer_dict[computer]) > longest_connection:
                        longest_connection = len(computer_dict[computer])

print("Dict written")
# 520 computers in the system
# each computer connects to 13 other computers
# the maximum possible size for a fully connected graph is 14
# the minimum is technically 3 (we've found a lot of triangles already)
# but running the combinatoric solver for a while it found a lot of 5s too (and then I stopped it because it took so long)

# let's get all 3 loops first
# we can then use these to assemble our larger clusters
# also prepare a hashmapped version of the computer dict for subset operations later

computer_set_dict = {}
found_loops = []
for computer in computer_dict.keys():
    computer_set_dict[computer] = set(computer_dict[computer])
    for first_connection in computer_dict[computer]:
        for second_connection in computer_dict[first_connection]:
            if computer in computer_dict[second_connection]:
                if not set([computer, first_connection, second_connection]) in found_loops: # sets since we don't care about order
                    found_loops.append(set([computer, first_connection, second_connection]))

print("Triangles found") # this finds 11011 triangles. big number
# a triangle is a fully connected 3-graph
# a fully connected n graph is made up of a fully connected n-1 graph with an additional element which is connected to each of the elements already present

current_subgraphs = found_loops
while len(current_subgraphs) > 1: # keep going until we only have 1 subgraph.
    # we're definitely done then because if it could be bigger we'll have all possible subgraphs of it
    print(len(current_subgraphs))
    new_subgraphs = set([]) # the magic ingredient to make it performant enough it to have this be a set too
    for j,subgraph in enumerate(current_subgraphs):
        # attempt to add another element

        # we find the new candidates by taking the intersection of all the connections of computers already in the graph
        candidates = []
        for i,computer in enumerate(subgraph):
            if i == 0:
                candidates = computer_set_dict[computer]
            else:
                candidates = candidates & computer_set_dict[computer]

        for computer in candidates:
            potential_set = frozenset(list(subgraph) + [computer]) # necessary to make this set immutable to add it to a set
            new_subgraphs.add(potential_set)
                    
    current_subgraphs = new_subgraphs

lan_party = list(list(current_subgraphs)[0])
lan_party.sort()
print(",".join(lan_party))