# import math

# Thaido1 = [5, 4, 3, 5, 3, 1, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 4, 5, 4, 4, 4, 5, 5, 4, 5, 4, 4, 4, 3, 4, 5, 4, 2, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 3, 3, 3, 4, 4, 4, 4, 3, 3, 5, 3, 5, 3, 4, 4, 3, 4, 5, 4, 5, 4, 4, 3, 4, 4, 4, 3, 3, 5, 4, 5, 3, 5, 5, 5, 4, 4, 3, 4, 4, 5, 4, 5, 5, 4, 5, 4, 4, 3, 5, 3, 5, 3, 3, 4, 5, 4, 4, 3, 3, 4, 1, 4, 5, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4, 5, 3, 5, 4, 4, 3, 3, 3, 5, 4, 4, 4, 1, 4, 4, 4, 4, 5, 5, 3, 4, 1, 4, 5, 5, 5, 3, 3, 4, 3, 4, 4, 4, 5, 3, 4, 3, 5, 4, 5, 5, 4, 4, 4, 4, 4, 4, 4, 5, 5]

# sum = 0
# for i in range(0, len(Thaido1)):
#     sum = sum + Thaido1[i]
    
# mean = sum/len(Thaido1)

# sum = 0
# for i in range(0, len(Thaido1)):
#     sum =  sum + Thaido1[i] - mean

# sum = math.sqrt(sum**2/(len(Thaido1) - 1))


# print(sum)

# import matplotlib.pyplot as plt

# num = 7
# x = []
# y = []

# count = 0

# while num != 1:
#     x.append(count)
#     y.append(num)
#     count += 1
#     if num % 2 == 0:
#         num = num / 2
#     else:
#         num = 3 * num + 1

# # Append the last value (which is 1) to the lists
# x.append(count)
# y.append(num)

# plt.plot(x, y)
# plt.xlabel('Step')
# plt.ylabel('Value')
# plt.title('Collatz Conjecture Sequence')
# plt.show()

# Function to read the file and extract variable values
def read_variables_from_file(filename):
    variables = {}
    with open(filename, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespace and split by '='
            name, value = line.strip().split(' = ')
            # Convert value to integer and store in dictionary
            variables[name] = int(value)
    return variables

# File containing the variables
filename = 'variables.txt'

# Read the variables from the file
variables = read_variables_from_file(filename)

# Assign the variables to specific names
a = variables.get('a')
b = variables.get('b')
c = variables.get('c')

# Print the variables to verify
print(f'a = {a}')
print(f'b = {b}')
print(f'c = {c}')


# a*X^2 + b*X + c = 0

delta = b**2 - 4*a*c

if (delta < 0):
    print("pt vo nghiem")
elif(delta == 0):
    print("pt co 1 nghiem")
else:
    print("pt co 2 nghiem")
    