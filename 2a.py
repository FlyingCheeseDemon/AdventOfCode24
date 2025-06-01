save_reports = 0

with open('2a-input.txt', 'r') as file:
    for line in file:
        levels = line.split(" ")
        sign = 0
        safety = True
        for i in range(len(levels)-1):
            num1 = int(levels[i])
            num2 = int(levels[i+1])
            diff = num2-num1
            if diff == 0:
                safety = False
                break
            if sign == 0:
                sign = diff/abs(diff)
            if diff/abs(diff) != sign:
                safety = False
                break
            if abs(diff) > 3 or abs(diff) < 1:
                safety = False
                break

        if safety:
            save_reports += 1

print(save_reports)