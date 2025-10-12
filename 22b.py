secret_numbers = []

with open('22-input.txt', 'r') as file:
    for line in file:
        secret_numbers.append(int(line[:-1]))

# let's implement mixing and pruning
def mix(a,b):
    return a ^ b

def prune(a):
    return a % 16777216 # 2**24

# precalculate all change arrays, takes just a few seconds for the big dataset
changes = []
prizes = []
for j,number in enumerate(secret_numbers):
    changes.append([])
    prizes.append([])
    secret = number
    price = number % 10
    for i in range(2000):
        # iterate on that number
        secret = prune(mix(secret,secret*64))
        secret = prune(mix(secret,int(secret/32)))
        secret = prune(mix(secret,secret*2048))
        new_price = secret % 10
        changes[j].append(new_price-price)
        prizes[j].append(new_price)
        price = new_price
        # all these multiplications and divisions are just bitshifts

print("done with generating changes")

# there is -9,....,9 to check for each entry 19**4 = 130321 checks of all the changes
# brute forcing and testing all combinations wasn't it, let's be smarter about it.
# for each monkey we generate a dictionary, the key of which is the input list of the change sequence and the output of which is the generated value

monkey_dict_list = []
for i,monkey_changes,monkey_prizes in zip(range(len(changes)),changes,prizes):
    monkey_dict_list.append({})
    for m in range(3,2000):
        key = str([monkey_changes[m-3],monkey_changes[m-2],monkey_changes[m-1],monkey_changes[m]])
        if key not in monkey_dict_list[i].keys():
            monkey_dict_list[i][key] = monkey_prizes[m]

print("Done with generating dicts")

best_bananas = 0
best_sequence = []
for i in range(-9,10):
    for j in range(-9,10):
        for k in range(-9,10):
            for l in range(-9,10):
                bananas = 0
                match_sequence = [i,j,k,l]
                # so we discard any sequence that cannot appear at all
                if abs(sum(match_sequence)) > 9 or abs(sum(match_sequence[:-1])) > 9 or abs(sum(match_sequence[1:])) > 9 or abs(sum(match_sequence[:2])) > 9 or abs(sum(match_sequence[1:3])) > 9 or abs(sum(match_sequence[2:])) > 9:
                    continue
                key = str(match_sequence)
                print(match_sequence)
                for monkey_dict in monkey_dict_list:
                    if key in monkey_dict.keys():
                        bananas += monkey_dict[key]

                if bananas > best_bananas:
                    best_bananas = bananas
                    best_sequence = match_sequence
                print(best_bananas)

print(best_bananas)
print(best_sequence)