# this is another job for linked lists!
class element():
    def __init__(self,number):
        self.file = number
        self.prev = None
        self.next = None

class double_linked_file_list():
    def __init__(self):
        self.first = None
        self.last = None

    def append(self,file):
        lmnt = element(file)
        if self.first == None:
            self.first = lmnt
            self.last = lmnt
        else:
            self.last.next = lmnt
            lmnt.prev = self.last
            self.last = lmnt

    def remove(self,lmnt):
        if lmnt.prev is not None:
            lmnt.prev.next = lmnt.next 
        else:
            self.first = lmnt.next

        if lmnt.next is not None:
            lmnt.next.prev = lmnt.prev
        else:
            self.last = lmnt.prev

    def insert_after(self,lmnt,pred):
        follow = pred.next

        pred.next = lmnt
        lmnt.prev = pred

        lmnt.next = follow
        if follow is not None:
            follow.prev = lmnt

    def __str__(self):
        txt = ""
        lnk = self.first
        while lnk:
            txt += str(lnk.file)
            txt += " "
            lnk = lnk.next
        return txt[:-1]
    
    def __len__(self):
        i = 0
        lmnt = self.first
        while lmnt is not None:
            i+=1
            lmnt = lmnt.next
        return i
    
stones = double_linked_file_list()
with open('11-input.txt', 'r') as file:
    for line in file:
        numbers = line[:-1].split(" ")

        for num in numbers:
            stones.append(int(num))

for blinks in range(25):
    # print(f"Blinked {blinks} times:")
    # print(stones)
    stone = stones.first
    while stone is not None:
        if stone.file == 0:
            stone.file = 1
        elif len(str(stone.file))%2 == 0:
            numstr = str(stone.file)
            half1 = numstr[:int(len(numstr)/2+0.5)]
            half2 = numstr[int(len(numstr)/2+0.5):]
            num1 = int(half1)
            num2 = int(half2)
            stone.file = num1
            newstone = element(num2)
            stones.insert_after(newstone,stone)
            stone = newstone
        else:
            stone.file *= 2024

        stone = stone.next


# print(f"Blinked {blinks+1} times:")
# print(stones)
print(len(stones))
