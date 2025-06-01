save_reports = 0

def safety_analyzer(levels):
    sign = 0
    for i in range(len(levels)-1):
        num1 = int(levels[i])
        num2 = int(levels[i+1])
        diff = num2-num1
        if diff == 0:
            return False
        if sign == 0:
            sign = diff/abs(diff)
        if diff/abs(diff) != sign:
            return False
        if abs(diff) > 3 or abs(diff) < 1:
            return False
        
    return True

with open('2a-input.txt', 'r') as file:
    for line in file:
        levels = line.split(" ")
        safety = safety_analyzer(levels)
        if not safety:
            # brute force through all possible levels if removing them helps
            for i in range(len(levels)):
                levels_reduced = levels[:i] + levels[i+1:]
                safety = safety_analyzer(levels_reduced)
                if safety:
                    break
        if safety:
            save_reports += 1

print(save_reports)