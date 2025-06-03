rules = []
all_pages = []

with open('5a-input.txt', 'r') as file:
    for line in file:
        if "|" in line:
            rules.append([int(num) for num in line[:-1].split("|")])
        elif "," in line:
            all_pages.append([int(num) for num in line[:-1].split(",")])

rule_dict = {}
# let's make a dictionary that for each number tells me which numbers are *not* allowed to come after them
for rule in rules:
    if str(rule[1]) in rule_dict.keys():
        rule_dict[str(rule[1])].append(rule[0])
    else:
        rule_dict[str(rule[1])] = [rule[0]]

# move this verification into it's own function for better readability
def verify_sequence(rule_dict,pages):
    illegal_pages = []
    for i,page in enumerate(pages):
        if page in illegal_pages:
            return False
        if str(page) in rule_dict.keys():
            illegal_pages += rule_dict[str(page)]
    return True

sum_of_middle_pages = 0
for pages in all_pages:
    is_valid = verify_sequence(rule_dict,pages)
    if is_valid:
        length = len(pages)
        middle = pages[int(length/2-0.5)]
        sum_of_middle_pages+=middle

print(sum_of_middle_pages)