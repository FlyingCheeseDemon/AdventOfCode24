keys = []
locks = []

with open('25-input.txt', 'r') as file:
    read_mode = "inputs"
    buffer = []

    for i,line in enumerate(file):
        if (i+1)%8 == 0:
            if buffer[0][0] == "#":
                # lock
                lock = [0]*5
                for i in range(5):
                    for j in range(1,7):
                        if buffer[j][i] == ".":
                            lock[i] = j-1
                            break
                        lock[i] = j
                locks.append(lock)
            else:
                # key
                key = [0]*5
                for i in range(5):
                    for j in range(0,6):
                        if buffer[6-j][i] == ".":
                            key[i] = j-1
                            break
                        key[i] = j
                keys.append(key)
            buffer = []
        else:
            buffer.append(list(line[:-1]))

print(locks)
print(keys)

score = 0
for key in keys:
    for lock in locks:
        fits = True
        for i in range(5):
            if key[i]+lock[i] > 5:
                fits = False
                break
        if fits:
            score += 1

print(score)