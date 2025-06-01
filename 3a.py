# this is an easy regex task, but can I solve it without using libraries....

text = ""
with open('3a-input.txt', 'r') as file:
    for line in file:
        text += line

# to match is "mul(***,***)" where *** is 1 to 3 numbers
result = 0

match = "mul(*,*)"

k = 0 # counts the position in the match we are in right now
comma_seen = False
numa = ""
numb = ""

i = 0
while i < len(text):

    if match[k] == "*" and text[i].isnumeric():
        if comma_seen:
            numb += text[i]
        else:
            numa += text[i]

        if len(numa) > 3 or len(numb) > 3:
            # one of the numbers is too long, try again
            k = 0
            comma_seen = False
            numa = ""
            numb = ""
            continue
    elif match[k] == "*":
        if text[i] == ',' and not comma_seen:
            comma_seen = True
            k += 2
        elif text[i] == ')':
            # we did it (probably), let's multiply
            if len(numa) != 0 and len(numb) != 0:
                result += int(numa) * int(numb)
            
            # and reset
            k = 0
            comma_seen = False
            numa = ""
            numb = ""
        else:
            i -= 1
            k = 0
            comma_seen = False
            numa = ""
            numb = ""
    elif text[i] == match[k]:
        k += 1
    else:
        # not matching the pattern, try again
        # but make sure your not missing the beginning of something new if we failed in the middle here
        if k != 0:
            i -= 1
        k = 0 
        comma_seen = False
        numa = ""
        numb = ""
        

    i += 1

print(result)
