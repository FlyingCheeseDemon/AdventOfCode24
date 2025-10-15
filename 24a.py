cables = {}
gates = []
output_length = 0

with open('24-input.txt', 'r') as file:
    read_mode = "inputs"
    for line in file:
        if line[0] == "\n":
            read_mode = "gates"
            continue
        if read_mode == "inputs":
            cable_name, value = line[:-1].split(": ")
            cables[cable_name] = int(value)
        else:
            input_1, operation, input_2, _, output = line[:-1].split(" ")
            cables[output] = -1
            gates.append([operation,input_1,input_2,output])
            if output[0] == "z":
                output_length += 1

output = [-1]*output_length
# print(cables)
# print(gates)

while not all([digit in [0,1] for digit in output]):
    for gate in gates:
        if cables[gate[1]] == -1 or cables[gate[2]] == -1:
            continue

        input_1 = cables[gate[1]]
        input_2 = cables[gate[2]]

        if gate[0] == "AND":
            out = int(bool(input_1) and bool(input_2))
        elif gate[0] == "XOR":
            out = int(bool(input_1) ^ bool(input_2))
        elif gate[0] == "OR":
            out = int(bool(input_1) or bool(input_2))
        else:
            print("what")

        cables[gate[3]] = out
        if gate[3][0] == "z":
            index = int(gate[3][1:])
            output[index] = out

output.reverse()
output = "".join([str(x) for x in output])
print(int(output, 2))