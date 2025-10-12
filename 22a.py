secret_numbers = []

with open('22-input.txt', 'r') as file:
    for line in file:
        secret_numbers.append(int(line[:-1]))

# let's implement mixing and pruning
def mix(a,b):
    return a ^ b

def prune(a):
    return a % 16777216 # 2**24

score = 0
for number in secret_numbers:
    secret = number
    for i in range(2000):
        # iterate on that number
        secret = prune(mix(secret,secret*64))
        secret = prune(mix(secret,int(secret/32)))
        secret = prune(mix(secret,secret*2048))
        # all these multiplications and divisions are just bitshifts
    score += secret

print(score)