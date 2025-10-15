import copy

cables = {}
gates = []
OUTPUT_LENGTH = 0

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
            gates.append([operation,{input_1,input_2},output])
            if output[0] == "z":
                OUTPUT_LENGTH += 1

# ok, brute forcing even one flip at a time is very slow and so far found no way to fix even the first bit.
# let's do this methodically

# each binary full adder has 5 gates usually
# the first one could be a half adder made of 2 gates
# so the minimum amount of gates this needs is 44*5+2 = 222 which is exactly the amount of gates we have.
# so we assume the circuit is made in the "normal" way

# instead of running the machine or testing inputs or whatever we verify the circuit diagram vs what we know an adder should be

# the half adder should be:
# x00 XOR y00 -> z00
# x00 AND y00 -> car0

# the full adders should be
# xnn XOR ynn -> cab1
# cab1 XOR carrym -> znn
# cab1 AND carrym -> cab2
# xnn AND ynn -> cab3
# cab2 OR cab3 -> carn

# with cab1,2,3 internal cables
# and carrym the carry from previously
# I don't *think* there's another way to do it in 5 gates

# based on this we can generate what the gate set for the adder *should* look like and then try to match the dummy names from me to the real cable names

# half adder

template_gates=[]
template_gates.append(["XOR",{"x00","y00"},"z00"])
template_gates.append(["AND",{"x00","y00"},"carry_0"])

# full adders
for i in range(1,45):
    index = "0"+str(i) if len(str(i)) == 1 else str(i)
    template_gates.append(["XOR",{"x"+index,"y"+index},f"cable1_{i}"])
    template_gates.append(["XOR",{f"cable1_{i}",f"carry_{i-1}"},"z"+index])
    template_gates.append(["AND",{f"cable1_{i}",f"carry_{i-1}"},f"cable2_{i}"])
    template_gates.append(["AND",{"x"+index,"y"+index},f"cable3_{i}"])
    if i == 44:
        template_gates.append(["OR",{f"cable2_{i}",f"cable3_{i}"},"z45"])
    else:
        template_gates.append(["OR",{f"cable2_{i}",f"cable3_{i}"},f"carry_{i}"])

# we test that the template circuit works for a few inputs
def machine(gates,input_1,input_2):

    input_1 = list(bin(input_1)[2:])
    input_1 = [int(i) for i in input_1]
    # print(input_1)
    input_1.reverse()
    for i in range(OUTPUT_LENGTH-1):
        key = "x" + ("0" + str(i) if len(str(i)) == 1 else str(i))
        try:
            cables[key] = int(input_1[i])
        except IndexError:
            cables[key] = 0
    
    input_2 = list(bin(input_2)[2:])
    input_2 = [int(i) for i in input_2]
    # print(input_2)
    input_2.reverse()
    for i in range(OUTPUT_LENGTH-1):
        key = "y" + ("0" + str(i) if len(str(i)) == 1 else str(i))
        try:
            cables[key] = int(input_2[i])
        except IndexError:
            cables[key] = 0

    # for key in cables.keys():
    #     if key[0] == "x" or key[0] == "y":
    #         print(key+": " + str(cables[key]))
        
    output = [-1]*OUTPUT_LENGTH
    timeout_cntr = len(gates)
    while not all([digit in [0,1] for digit in output]) and timeout_cntr > 0:
        for gate in gates:

            # input_1 = cables[gate[1]]
            # input_2 = cables[gate[2]]
            
            input_1,input_2 = list(gate[1])
            if cables[input_1] == -1 or cables[input_2] == -1:
                continue

            if gate[0] == "AND":
                out = int(bool(cables[input_1]) and bool(cables[input_2]))
            elif gate[0] == "XOR":
                out = int(bool(cables[input_1]) ^ bool(cables[input_2]))
            elif gate[0] == "OR":
                out = int(bool(cables[input_1]) or bool(cables[input_2]))
            else:
                print("what")

            cables[gate[2]] = out
            if gate[2][0] == "z":
                index = int(gate[2][1:])
                output[index] = out
        timeout_cntr -= 1

    if timeout_cntr < 0:
        raise Exception

    # return [str(x) for x in output]

    output.reverse()
    output = "".join([str(x) for x in output])
    return int(output, 2)

# print(machine(template_gates,20,1))

# now for each cable in the template we have to find the corresponding cable in the real thing
# and some of them will not work because we have those 4 flips

GLOBAL_CABLE_MAP = {} # dictionary (contains both the forward and backwards direction)

def map_cables(test_cable,cable_map):
    if test_cable[0] in "xyz":
        return test_cable
    else:
        return cable_map[test_cable]

# template_gates is a global constant and will not be changed anymore
def test_gates(gates,flips): # flips is a dictionary that assigns every cable it's flip
    cable_map = {}
    for i,gate in enumerate(template_gates):
        # these are already in order so they only depend on things defined before
        # as long as we don't hit a flip this will run
        # inputs = list(gate[1])
        inputs = gate[1]
        # input_1,input_2 = inputs
        output = gate[2]
        gate_type = gate[0]
        found_it = False
        for testgate in gates:
            if gate_type != testgate[0]:
                continue
            try:
                testinputs = {map_cables(inp,cable_map) for inp in testgate[1]}
                testoutput = testgate[2]
                if testoutput in flips.keys():
                    testoutput = flips[testoutput]

                if testinputs == inputs:
                    cable_map[testoutput] = output
                    cable_map[output] = testoutput
                    if ((output[0] == "z") and (testoutput[0] == "z") or (output[0] != "z") and (testoutput[0] != "z")):
                        # print(f"{gate} = {testgate}")
                        found_it = True
                        break
                    else:

                        print(f"output ERROR @ {i}: {gate}")
                        return [cable_map[testoutput]], cable_map, i, "output", False
            except KeyError:
                pass

        if not found_it:
            print(f"input ERROR @ {i}: {gate}")
            potential_errors = gate[1]
            potential_errors_inv = [cable_map[cable] for cable in potential_errors]
            return potential_errors_inv, cable_map, i, "input", False
        
    return [],cable_map,i,"",True

def get_potential_cables(current_map):
    potential_cables = set([])
    for cable in cables:
        if cable not in current_map.keys():
            potential_cables.add(cable)
    return potential_cables


success = False
flips = {}
while not success:
    potential_errors, resulting_map, current_errorpos, io, success = test_gates(gates,flips)
    if io == "output":
        problem_cable = potential_errors[0] # there will only be 1
        problem_inv = resulting_map[problem_cable] # the z cables are all called the same in both worlds. so we can just swap these two
        flips[problem_cable] = problem_inv
        flips[problem_inv] = problem_cable
        print(f"flipping {problem_inv} and {problem_cable}")
    elif io == "input":
        print("Initializing tryout of flips")
        for candidate in potential_errors:
            potential_flip_targets = get_potential_cables(resulting_map)
            for potential_target in potential_flip_targets:
                temp_flips = copy.copy(flips)
                temp_flips[candidate] = potential_target
                temp_flips[potential_target] = candidate
                _, _, new_errorpos, _, success = test_gates(gates,temp_flips)
                if success:
                    print("Victory!")
                    print(flips)
                    break
                if new_errorpos > current_errorpos:
                    print(f"flipping {candidate} and {potential_target}")
                    flips = temp_flips
                    break
            if success or new_errorpos > current_errorpos:
                break

answer = list(flips.keys())
answer.sort()
print(",".join(answer))