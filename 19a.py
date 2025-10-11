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

def find_towel_at_beginning(pattern):
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
        if len(pattern) == towel_length:
            return True
        options.append(towel)
    if len(options) == 0:
        return False
    truths = []
    for towel in options:
        pattern_copy = pattern[len(towel):]
        truths.append(find_towel_at_beginning(pattern_copy))
        if any(truths):
            break
    if any(truths):
        return True   
    else:
        return False 

counter = 0
for i,pattern in enumerate(patterns_to_generate):
    print(f"{i+1}/{len(patterns_to_generate)}")
    if find_towel_at_beginning(pattern):
        print("yep")
        counter += 1
    else:
        print("nah")

print(counter)