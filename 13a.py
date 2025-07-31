machines = [] 

cost_A = 3
cost_B = 1

with open('13-input.txt', 'r') as file:
    i = 0
    machine = [None]*3
    for line in file:
        if i != 3:
            half1, half2 = line.split(",")
            num1 = half1[9 if i == 2 else 12:]
            num2 = half2[3:-1]
            machine[i] = [int(num1),int(num2)]
        else:
            machines.append(machine)
            machine = [None]*3
        i += 1
        i %= 4
    machines.append(machine)

tokens = 0

for machine in machines:
    A = machine[0]
    B = machine[1]
    P = machine[2]

    if A[0] == 0:
        y = P[0]*1./B[0]
        x = (P[1]-y*B[1])/A[1]
    elif A[1] == 0:
        y = P[1]*1./B[1]
        x = (P[0]-y*B[0])/A[0]
    else:
        y = 1.*(P[0]-P[1]*A[0]/A[1])/(B[0]-B[1]*A[0]/A[1])
        x = (P[0]-y*B[0])/A[0]

    x = round(x,2) # to avoid floating point errors in the comparison below
    y = round(y,2)

    if int(x) != x or int(y) != y or x < 0 or y < 0:
        print(x,y, "unsolvable")
        continue
    
    print(x,y)
    tokens += x*cost_A + y*cost_B

print(tokens) # 28753