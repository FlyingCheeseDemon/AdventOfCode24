# alright, I think we do not want to actually expand the thing in order to do this
# that sounds like a terrible idea
# let's try to be smart about it
# every empty space actually just means taking stuff from the end of the file instead of the front.
cks = 0

with open('9-input.txt', 'r') as file:
    for line in file:
        line = [int(n) for n in line[:-1]]

# the file id we are at at the front or back
id_front = 0
id_back = int(len(line)/2-0.5) # every second number is a file block, so the last index is that
inx_back = len(line)-1
counter_back = 0

# our memory pointers.
max_mem_pt = sum(line[::2]) 
mem_pt = 0

done = False

for inx_front,value in enumerate(line): # i is the position in the input
    # all of this is nice until we reach the point in the middle. we have to stop in time
    if inx_front%2 == 0:
        # read from the front
        for t in range(value):
            cks += id_front*mem_pt
            mem_pt += 1
            if mem_pt >= max_mem_pt:
                done = True
                break
        id_front += 1
    else:
        # read from the back
        for t in range(value):
            cks += id_back*mem_pt
            mem_pt += 1
            counter_back += 1
            if counter_back >= line[inx_back]:
                id_back -= 1
                counter_back = 0
                inx_back -= 2
            if mem_pt >= max_mem_pt:
                done = True
                break

    if done:
        break

print(cks)