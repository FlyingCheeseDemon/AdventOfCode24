results = []
numbers = []

with open('7-input.txt', 'r') as file:
    for line in file:
        result, numbers_chars = line.split(":")
        results.append(int(result))
        numbers_chars = numbers_chars[1:-1].split(" ")
        numbers_int = [int(num) for num in numbers_chars]
        numbers.append(numbers_int)

def concat(num1,num2):
    return int(str(num1)+str(num2))

def does_it_work(target,current_value,remaining_numbers):
    if len(remaining_numbers) == 0:
        return current_value == target

    test_multiply = does_it_work(target,current_value*remaining_numbers[0],remaining_numbers[1:])
    test_add = does_it_work(target,current_value+remaining_numbers[0],remaining_numbers[1:])
    test_concat = does_it_work(target,concat(current_value,remaining_numbers[0]),remaining_numbers[1:])
    return test_add or test_multiply or test_concat

total_sum = 0
for result,number in zip(results,numbers):
    if does_it_work(result,number[0],number[1:]):
        total_sum += result

print(total_sum)