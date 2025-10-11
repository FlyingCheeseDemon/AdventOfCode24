available_towels = []
patterns_to_generate = []

with open("19-input.txt") as file:
    for i,line in enumerate(file):
        if i == 0:
            available_towels = line[:-1].split(", ")
        elif i == 1:
            continue # nothing here
        else:
            patterns_to_generate.append(line[:-1])

print(available_towels)
print(patterns_to_generate)
MEMO = {}

def find_towel_at_beginning(pattern):
    if pattern in MEMO:
        return MEMO[pattern]
    options = []
    for towel in available_towels:
        towel_length = len(towel)
        if len(pattern) < towel_length:
            continue
        matched = True
        for i in range(towel_length):
            if pattern[i] != towel[i]:
                matched = False
                break
        if not matched:
            continue
        options.append(towel)
    if len(options) == 0:
        return 0
    counter = 0
    for towel in options:
        if len(pattern) == len(towel):
            counter += 1
        else:
            pattern_copy = pattern[len(towel):]
            counter += find_towel_at_beginning(pattern_copy)
    MEMO[pattern] = counter
    return counter

counter = 0
for i,pattern in enumerate(patterns_to_generate):
    print(f"{i+1}/{len(patterns_to_generate)}")
    counter += find_towel_at_beginning(pattern)

print(counter)