# this one's gonna work completely differently....
# let's represent the memory as a list, but differently
cks = 0

with open('9-input.txt', 'r') as file:
    for line in file:
        line = [int(n) for n in line[:-1]]

print(len(line))

class element():
    def __init__(self,file):
        self.file = file
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
            lnk = lnk.next
        return txt
    
    # def __str__(self):
    #     txt = ""
    #     inx = 0
    #     lnk = self.first
    #     while lnk:
    #         while inx < lnk.file[0]:
    #             txt += '.'
    #             inx += 1
    #         for i in range(lnk.file[1]):
    #             txt += str(lnk.file[2])
    #             inx += 1

    #         lnk = lnk.next
    #     return txt
    
    def __len__(self):
        i = 0
        lmnt = self.first
        while lmnt is not None:
            i+=1
            lmnt = lmnt.next
        return i

# build the inital memory list
# the list shows the memory in order, each element contains [start_index,length_of_data,file_id] 

memory = double_linked_file_list()

file_id = 0
current_index = 0
for i,value in enumerate(line):
    if i%2 == 0:
        new_file = [current_index,value,file_id]
        current_index += value
        file_id += 1
        memory.append(new_file)
    else:
        # theres whitespace to consider
        current_index += value

print(len(memory))

def compression_step(memory,file_id):
    # find the next file to move
    # searching from the back is probably faster because we are looking for ids in descending order
    file = memory.last
    while file.file[2] != file_id:
        file = file.prev

    needed_space = file.file[1]

    file_0 = memory.first
    file_1 = file_0.next
    while True:
        if file_0.file[2] == file.file[2]:
            # we haven't found anything until we hit our own file again. nothing happens this step
            done_stuff = False
            break

        blank_space = file_1.file[0]-file_0.file[0]-file_0.file[1]
        if needed_space <= blank_space:
            new_index = file_0.file[0]+file_0.file[1]
            file.file[0] = new_index
            # sort the thing again
            # this is why we use the dll. cause with an array it's a _mess_
            memory.remove(file)
            memory.insert_after(file,file_0)

            done_stuff = True
            break
        file_1 = file_1.next
        file_0 = file_0.next

    return memory, file_id - 1,done_stuff

file_id -= 1
# print(memory)
while file_id > 0:
    memory,file_id,done_stuff = compression_step(memory,file_id)
    if done_stuff:
        pass
        # print(memory)

lnk = memory.first
while lnk is not None:
    # reminder link.file has the structure [start_indx,length,file_id]
    for i in range(lnk.file[1]):
        cks += lnk.file[2]*(i+lnk.file[0])
    lnk = lnk.next

print(cks)