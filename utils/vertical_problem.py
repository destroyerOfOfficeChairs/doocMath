import random

import utils.latex
import utils.operands

from jinja2 import Template

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
    output = output[1:]
    return output

def create_answer_row(num, col_count, solve):
    output = "\\multicolumn{" + str(col_count) + "}{c}{ }"
    if solve:
        output = "\\multicolumn{" + str(col_count) + "}{c}{" + str(num) + "}"
    return output

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

def create_vertical_problem(args):
    digits_flag = args.digits > 0
    operator = choose_operator(args.worksheet)
    operands = utils.operands.create_two_operands(args, operator)
    a = operands[0]
    b = operands[1]
    col_spec = ""
    col_count = 0
    if digits_flag:
        col_spec = utils.latex.create_column_spec(args.digits + 1)
        col_count = args.digits + 1
    else:
        col_spec = utils.latex.create_column_spec(max(args.digits_A, args.digits_B) + 1)
        col_count = max(args.digits_A, args.digits_B) + 1
    row_1 = " " + create_row(a, col_count)
    row_2 = operator + create_row(b, col_count)
    answer = 0;
    row_3 = create_answer_row(answer, col_count, False)
    match operator:
        case "+":
            answer = a + b
        case "-":
            answer = a - b
        case "x":
            answer = a * b
    answered_row_3 = create_answer_row(answer, col_count, True)

    if args.no_expand:
        col_spec = "r r"
        row_1 = f"&{str(a)}"
        row_2 = f"{operator}&{str(b)}"
        row_3 = " "
        answered_row_3 = "&" + str(answer)

    with open("templates/vertical_problem.j2") as file:
        template = Template(file.read(), variable_start_string='<<', variable_end_string='>>')
    rendered_problem = template.render(col_spec=col_spec, row_1=row_1, row_2=row_2, row_3=row_3)
    rendered_solution = template.render(col_spec=col_spec, row_1=row_1, row_2=row_2, row_3=answered_row_3)
    return [rendered_problem, rendered_solution]
