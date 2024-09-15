import argparse
import datetime
import os
import random
import subprocess
import sys
import textwrap
from jinja2 import Template

TITLES = {
    "add": "ADDITION",
    "sub": "SUBTRACTION",
    "addsub": "ADDITION AND SUBTRACTION",
    "mult": "MULTIPLICATION",
    "borrow": "SUBTRACTION - BORROW",
    "carry-over": "ADDITION - CARRY OVER"
}

def handle_args():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
        Welcome to doocMath! You can use this program to create math worksheets for your kids."""),
        usage=textwrap.dedent("""
        Use case #1:
        %(prog)s --worksheet [WORKSHEET] --digits [1-5] [OPTIONAL ARGS]
        
        Use case #2:
        %(prog)s --worksheet [WORKSHEET] --digits-in-operand-A [1-5] --digits-in-operand-B [1-5] [OPTIONAL ARGS]

        Example #1:
        %(prog)s --worksheet addsub --digits 3

        Example #2:
        %(prog)s --worksheet sub --digits-in-operand-A 2 --digits-in-operand-B 1"""),
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "--worksheet",
        required=True,
        choices=["add", "sub", "addsub", "mult", "borrow", "carry-over"],
        help=textwrap.dedent("""\
    The type of worksheet you would like to create. Supported types are:
    add - contains addition problems
    sub - contains subtraction problems
    addsub - contains addition and subtraction problems
    mult - contains multiplication problems
    borrow - contains subtraction problems where every solution requires borrowing
    carry-over - contains addition problems where every solution requires carrying over
    
    """))
    
    parser.add_argument(
        "--digits",
        type=int,
        choices=[1,2,3,4],
        default=0,
        help=textwrap.dedent("""\
    The maximum number of digits you would like each operand to have.

    You must use either this argument, or both --digits-in-operand-A AND --digits-in-operand-B.

    Using this argument negates BOTH --digits-in-operand-A AND --digits-in-operand-B.
    
    """))
    
    parser.add_argument(
        "--digits-A",
        type=int,
        choices=[1,2,3,4],
        default=0,
        help=textwrap.dedent("""\
    The maximum number of digits you would like the first operand to have.
    A + B
    A - B
    A * B
    
    """))
    
    parser.add_argument(
        '--digits-B',
        type=int,
        choices=[1,2,3,4],
        default=0,
        help=textwrap.dedent("""\
    The maximum number of digits you would like the second operand to have.
    A + B
    A - B
    A * B
    
    """))
    
    def check_pages(value):
        ivalue = int(value)
        if ivalue < 1 or ivalue > 100:
             raise argparse.ArgumentTypeError("Number of pages must be between 1 and 100.")
        return ivalue

    parser.add_argument(
        "--pages",
        type=check_pages,
        default=1,
        help=textwrap.dedent("""\
        The number of pages you would like the worksheet PDF to have.""")
    )

    parser.add_argument(
        "--keep-all",
        action="store_true",
        help=textwrap.dedent("""\
        By default, only a .pdf file is produced by doocMath.
        If you would like to preserve the .tex, .aux, and .log files,
        then you can use this argument as a boolean flag.""")
    )

    args = parser.parse_args()

    if ((args.digits > 0 and (args.digits_A > 0 or args.digits_B > 0)) or
        (args.digits == 0 and args.digits_A == 0 and args.digits_B == 0)):
        parser.error("""Use EITHER --digits OR BOTH --digits-in-operand-A AND --digits-in-operand-B""")

    return args

def create_column_spec(num):
    output = ""
    for i in range(num):
        output = output + " c"
    output = output.strip()
    return output

def create_row(num, col_count):
    num_string = str(num)
    msd_index = col_count - len(num_string)
    counter = 0
    output = ""
    for i in range(col_count):
        temp = " "
        if i >= msd_index:
            temp = num_string[counter]
            counter += 1
        output = output + "&" + temp
    output = output[2:]
    return output

def generate_operand(digits):
    upper_string = ""
    for i in range(digits):
        upper_string = upper_string + "9"
    upper = int(upper_string)
    return random.randint(1, upper)

def choose_operator(worksheet):
    operator = ""
    if worksheet == "add" or worksheet == "carry-over":
        operator = "+"
    elif worksheet == "sub" or worksheet == "borrow":
        operator = "-"
    elif worksheet == "addsub":
        operator = random.choice(["+", "-"])
    elif worksheet == "mult":
        operator = "x"
    else:
        print("Something has gone terribly wrong")
        sys.exit()
    return operator

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

def create_vertical_problem(args):
    digits_flag = args.digits > 0
    a = 0
    b = 0
    col_spec = ""
    col_count = 0
    operator = choose_operator(args.worksheet)
    sub_flag = operator == "-"
    if digits_flag:
        a = generate_operand(args.digits)
        b = generate_operand(args.digits)
        col_spec = create_column_spec(args.digits + 1)
        col_count = args.digits + 1
    else:
        a = generate_operand(args.digits_A)
        b = generate_operand(args.digits_B)
        col_spec = create_column_spec(max(args.digits_A, args.digits_B) + 1)
        col_count = max(args.digits_A, args.digits_B) + 1
    if sub_flag and b > a:
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
    row_1 = " " + create_row(a, col_count)
    row_2 = operator + create_row(b, col_count)
    with open("templates/vertical_problem.j2") as file:
        template = Template(file.read(), variable_start_string='<<', variable_end_string='>>')
    rendered_problem = template.render(col_spec=col_spec, row_1=row_1, row_2=row_2)
    return rendered_problem

def get_template_file_path(args):
    # For now, it just returns one thing
    return "templates/worksheet_grid.j2"

def render_worksheet(args):
    template_file_path = get_template_file_path(args)
    with open(template_file_path) as file:
        template = Template(file.read(), variable_start_string='<<', variable_end_string='>>', block_start_string='<%', block_end_string='%>')
    outer_col_count = 4
    outer_row_count = 4
    col_spec = create_column_spec(outer_col_count)
    content = [[[create_vertical_problem(args) for i in range(outer_col_count)] for j in range(outer_row_count)] for k in range(args.pages)]
    rendered_worksheet = template.render(col_spec=col_spec, content=content, title=TITLES[args.worksheet])
    return rendered_worksheet

def generate_output_directory(worksheet):
    # Create a timestamped directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{worksheet}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def compile_latex(output_dir, tex_file_name):
    # Change directory to the output directory
    current_dir = os.getcwd()
    os.chdir(output_dir)

    # Run lualatex to compile the LaTeX file
    try:
        subprocess.run(["lualatex", tex_file_name], check=True)
    finally:
        # Change back to the original directory
        os.chdir(current_dir)

def delete_extra_files(output_dir):
    base = output_dir + "/" + output_dir
    aux_file = base + ".aux"
    log_file = base + ".log"
    tex_file = base + ".tex"
    os.remove(aux_file)
    os.remove(log_file)
    os.remove(tex_file)

def main():
    args = handle_args()
    rendered_worksheet = render_worksheet(args)
    output_dir = generate_output_directory(args.worksheet)
    tex_file_name = output_dir + ".tex"
    tex_file_path = output_dir + "/" + tex_file_name
    with open(tex_file_path, mode="w") as file:
        file.write(rendered_worksheet)
    compile_latex(output_dir, tex_file_name)
    if not args.keep_all:
        delete_extra_files(output_dir)

if __name__ == "__main__":
    main()
