list1 = []
list2 = []

# read both lists
with open('1a-input.txt', 'r') as file:
    for line in file:
        text = line.split("   ")
        list1.append(int(text[0]))
        list2.append(int(text[1]))

similarity_score = 0
for i in range(len(list1)):
    for j in range(len(list2)):
        if list2[j] == list1[i]:
            similarity_score += list1[i]

print(similarity_score)