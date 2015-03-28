lst = [0, 1]

def last_two_sum(list):
    global lst
    for i in range(1, len(list)):
        last = list[i]
        second_to_last = list[i-1]
        sum = last + second_to_last
    lst.append(sum)
    return lst


for i in range(40):
    print last_two_sum(lst)