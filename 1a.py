list1 = []
list2 = []

# read both lists
with open('1a-input.txt', 'r') as file:
    for line in file:
        text = line.split("   ")
        list1.append(int(text[0]))
        list2.append(int(text[1]))

total_difference = 0

while len(list1)>0:
    #find smallest element in each list
    smallest1 = list1[0]
    inx1 = 0
    smallest2 = list2[0]
    inx2 = 0
    for i in range(len(list1)):
        if list1[i] < smallest1:
            smallest1 = list1[i]
            inx1 = i
        if list2[i] < smallest2:
            smallest2 = list2[i]
            inx2 = i
    
    print(f"1: {smallest1}; 2: {smallest2}")
    total_difference += abs(smallest1-smallest2)
    list1[inx1] = list1[-1]
    list1 = list1[:-1]
    list2[inx2] = list2[-1]
    list2 = list2[:-1]

print(total_difference)