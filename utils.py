# Function to check if all elements in a list are zeros between start and end
def check_zeros(lst, start, end):
    return all(x == 0 for x in lst[start:end])

def switch_values(lst, start, end):
    lst[start:end] = reversed(lst[start:end])
