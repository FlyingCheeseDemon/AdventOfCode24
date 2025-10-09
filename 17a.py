with open('17-input.txt', 'r') as file:
    for i,line in enumerate(file):
        if i == 3:
            continue
        information = line.split(" ")[-1][:-1]
        if i == 0:
            regA = int(information)
        elif i == 1:
            regB = int(information)
        elif i == 2:
            regC = int(information)
        else:
            program = information.split(",")
    
print(regA)
print(regB)
print(regC)
print(program)
print()

regs = [regA,regB,regC]

def get_combo_operand(n,regs):
    if n < 4:
        return n
    else:
        return regs[n-4]

instr_ptr = 0
output = []
while instr_ptr < len(program)-1:
    opcode = int(program[instr_ptr])
    arg = int(program[instr_ptr+1])
    if opcode == 0:
        # print("adv")
        result = int(regs[0]/(2**get_combo_operand(arg,regs)))
        regs[0] = result
    elif opcode == 1:
        # print("bxl")
        result = regs[1] ^ arg
        regs[1] = result
    elif opcode == 2:
        # print("bst")
        result = get_combo_operand(arg,regs)%8
        regs[1] = result
    elif opcode == 3:
        # print("jnz")
        if regs[0] == 0:
            pass
        else:
            instr_ptr = arg
            continue
    elif opcode == 4:
        # print("bxc")
        result = regs[1] ^ regs[2]
        regs[1] = result
    elif opcode == 5:
        # print("out")
        result = get_combo_operand(arg,regs)%8
        output.append(result)
    elif opcode == 6:
        # print("bdv")
        result = int(regs[0]/(2**get_combo_operand(arg,regs)))
        regs[1] = result
    elif opcode == 7:
        # print("cdv")
        result = int(regs[0]/(2**get_combo_operand(arg,regs)))
        regs[2] = result
    else:
        print(f"Critical Error at instr_ptr = {instr_ptr}")
        print(f"Opcode: {opcode}")
        print(f"Argument: {arg}")
        print(f"RegA: {regs[0]}")
        print(f"RegB: {regs[1]}")
        print(f"RegC: {regs[2]}")
        break

    instr_ptr += 2

output_txt = ""
for element in output:
    output_txt += str(element) + ","
output_txt = output_txt[:-1]
print(output_txt)

print(f"RegA: {regs[0]}")
print(f"RegB: {regs[1]}")
print(f"RegC: {regs[2]}")