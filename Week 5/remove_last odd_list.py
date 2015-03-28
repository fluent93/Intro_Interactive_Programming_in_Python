#remove the last odd element of the list.
#If you directly access the odd element, not index using 'range',
#you meet an error. We have three '7's. Even if you go through
#the end of the list and the last odd element should be 7 of index 14, 
#but it always points to the 7 of index 1.

def remove_last_odd(numbers):
    has_odd = False
    last_odd_idx = 0
    for i in range(len(numbers)):
        if numbers[i] % 2 == 1:
            has_odd = True
            last_odd_idx = i
            print last_odd_idx
            
    if has_odd:
        numbers.pop(last_odd_idx)
        
        
numbers = [1,7,2,34,8,7,2,5,14,22,93,48,76,15,7]
    
remove_last_odd(numbers)
print numbers