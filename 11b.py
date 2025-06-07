# well, to get to 75 we need to be more performant....
# the order of the stones doesn't actually matter
# we don't even have to do all of them at once, we can just look at each stone, do the procedure and record how many stones there are in the end

# the process is completely deterministic.
# if I have the score for a certain number,depth pair already I can return that immediately without searching deeper.
# let's make it a dictionary for that O(1) lookup
found_pairs = {} # [number,depth,score]
DEPTH = 75


def process_stone(number,depth):
    if f"{number},{depth}" in found_pairs.keys():
        return found_pairs[f"{number},{depth}"]
    if depth == DEPTH:
        return 1
    if number == 0:
        score = process_stone(1,depth+1)
        found_pairs[f"{number},{depth}"] = score
        return score
    elif len(str(number))%2 == 0:
        numstr = str(number)
        num1 = int(numstr[:int(len(numstr)/2+0.5)])
        num2 = int(numstr[int(len(numstr)/2+0.5):])
        score = process_stone(num1,depth+1) + process_stone(num2,depth+1)
        found_pairs[f"{number},{depth}"] = score
        return score
    else:
        score = process_stone(number*2024,depth+1)
        found_pairs[f"{number},{depth}"] = score
        return score

stones = []
with open('11-input.txt', 'r') as file:
    for line in file:
        numbers = line[:-1].split(" ")

        for num in numbers:
            stones.append(int(num))

amount_stones = 0

for stone in stones:
    print(f"Working on stone {stone}")
    amount_stones+=process_stone(stone,0)

print(amount_stones)
