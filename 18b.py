# we binary search this.
# might still take some time, but better than doing it linearly
# we know at 1024 it still works so that's our lower startpoint.

testing = False

def machine(n,testing):

    memory = []
    size = (7 if testing else 71)
    for i in range(size):
        line = ["."]*(size)
        memory.append(line)

    with open(('18-test.txt' if testing else '18-input.txt'), 'r') as file:
        for i,line in enumerate(file):
            if i == n:
                break

            X,Y = line[:-1].split(",")
            X = int(X)
            Y = int(Y)
            memory[Y][X] = "#"

    def print_maze(maze):
        for line in maze:
            ln = ""
            for character in line:
                ln += character
                if len(character) < 2:
                    ln += " "
            print(ln)

    start = [0,0]
    end = [size-1,size-1]
    memory[0][0] = "0"

    found_stuff = True
    n = 0
    while found_stuff:
        found_stuff = False
        for i in range(size):
            for j in range(size):
                if memory[i][j] != ".":
                    continue
                candidates = []
                if i != 0:
                    try:
                        value = int(memory[i-1][j])
                        candidates.append(value)
                    except:
                        pass
                if i != size-1:
                    try:
                        value = int(memory[i+1][j])
                        candidates.append(value)
                    except:
                        pass
                
                if j != 0:
                    try:
                        value = int(memory[i][j-1])
                        candidates.append(value)
                    except:
                        pass
                if j != size-1:
                    try:
                        value = int(memory[i][j+1])
                        candidates.append(value)
                    except:
                        pass
                
                if len(candidates) != 0:
                    if n in candidates:
                        found_stuff = True
                        memory[i][j] = str(n+1)

        n += 1

    print(memory[size-1][size-1])
    return memory[size-1][size-1]

lower = (12 if testing else 1024)
with open(('18-test.txt' if testing else '18-input.txt'), 'r') as file:
    for i,line in enumerate(file):
        pass
    upper = i

while True:
    pos_to_test = int((upper+lower)/2)

    result = machine(pos_to_test,testing)
    try:
        length = int(result)
        lower = pos_to_test
    except:
        upper = pos_to_test

    if upper-lower == 1:
        break

with open(('18-test.txt' if testing else '18-input.txt'), 'r') as file:
    for i,line in enumerate(file):
        if i == lower:
            print(line)
