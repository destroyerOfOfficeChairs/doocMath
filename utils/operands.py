import random

def generate_operand(digits):
    upper_string = ""
    for i in range(digits):
        upper_string = upper_string + "9"
    upper = int(upper_string)
    return random.randint(1, upper)

def create_two_operands(args, operator=None):
    digits_flag = args.digits > 0
    a = 0
    b = 0
    if digits_flag:
        a = generate_operand(args.digits)
        b = generate_operand(args.digits)
    else:
        a = generate_operand(args.digits_A)
        b = generate_operand(args.digits_B)
    if operator == "-" and b > a:
        temp = a
        a = b
        b = temp
    if args.worksheet == "borrow":
        arr = create_borrow_subtraction_operands(a ,b)
        a = arr[0]
        b = arr[1]
    if args.worksheet == "carry-over":
        arr = create_carry_over_addition_operands(a, b)
        a = arr[0]
        b = arr[1]
    return [a, b]

def create_borrow_subtraction_operands(a, b):
    arr_a = list(str(a))
    arr_b = list(str(b))
    digits_in_A = len(arr_a)
    digits_in_B = len(arr_b)
    number_of_indexes = min(digits_in_A, digits_in_B)
    if number_of_indexes == digits_in_A:
        number_of_indexes -= 1
    index = -1
    counter = 0
    while counter < number_of_indexes:
        if int(arr_a[index]) >= int(arr_b[index]):
            if int(arr_a[index]) == 9:
                arr_a[index] = str(int(arr_a[index]) - 1)
            elif int(arr_a[index]) == 0:
                arr_b[index] = str(int(arr_b[index]) + 1)
            else:
                arr_a[index] = str(int(arr_a[index]) - 1)
                arr_b[index] = str(int(arr_b[index]) + 1)
            index += 1
            counter -= 1
        index -= 1
        counter += 1
    str_a = ''.join(arr_a)
    str_b = ''.join(arr_b)
    if digits_in_A == digits_in_B and int(str_a) < int(str_b):
        if int(str_a[0]) == 9:
            arr_b[0] = str(int(arr_b[0]) - 1)
        elif int(str_a[1]) == 1:
            arr_a[0] = str(int(arr_a[0]) + 1)
        else:
            arr_a[0] = str(int(arr_a[0]) + 1)
            arr_b[0] = str(int(arr_b[0]) - 1)
        str_a = ''.join(arr_a)
        str_b = ''.join(arr_b)
    return [int(str_a), int(str_b)]

def create_carry_over_addition_operands(a, b):
    new_a = a
    new_b = b
    had_to_switch = False
    if new_a < new_b:
        temp = new_a
        new_a = new_b
        new_b = temp
        had_to_switch = True
    arr_a = list(str(new_a))
    arr_b = list(str(new_b))
    digits_in_A = len(arr_a)
    digits_in_B = len(arr_b)
    number_of_indexes = min(digits_in_A, digits_in_B)
    if number_of_indexes == digits_in_A:
        number_of_indexes -= 1
    index = -1
    counter = 0
    while counter < number_of_indexes:
        if int(arr_a[index]) + int(arr_b[index]) < 10:
            if int(arr_a[index]) == 9:
                arr_b[index] = str(int(arr_b[index]) + random.randint(1, 9))
            elif int(arr_b[index]) == 9:
                arr_a[index] = str(int(arr_a[index]) + random.randint(1, 9))
            else:
                arr_a[index] = str(random.randint(1, 9))
                arr_b[index] = str(random.randint(1, 9))
            index += 1
            counter -= 1
        index -= 1
        counter += 1
    str_a = ''.join(arr_a)
    str_b = ''.join(arr_b)
    if had_to_switch:
        temp = str_a
        str_a = str_b
        str_b = temp
    return [int(str_a), int(str_b)]
