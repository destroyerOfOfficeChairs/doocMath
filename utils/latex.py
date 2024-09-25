import utils.vertical_problem
import utils.long_div

from jinja2 import Template

TITLES = {
    "add": "ADDITION",
    "sub": "SUBTRACTION",
    "addsub": "ADDITION AND SUBTRACTION",
    "mult": "MULTIPLICATION",
    "borrow": "SUBTRACTION - BORROW",
    "carry-over": "ADDITION - CARRY OVER",
    "long-div": "LONG DIVISION",
}

def create_column_spec(num):
    output = ""
    for i in range(num):
        output = output + " c"
    output = output.strip()
    return output

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
    if args.worksheet != "long-div":
        content = []
        answer_content = []
        for i in range(args.pages):
            content.append([])
            answer_content.append([])
            for j in range(outer_row_count):
                content[i].append([])
                answer_content[i].append([])
                for k in range(outer_col_count):
                    arr = utils.vertical_problem.create_vertical_problem(args)
                    content[i][j].append(arr[0])
                    answer_content[i][j].append(arr[1])
    else:
        content = []
        answer_content = []
        for i in range(args.pages):
            content.append([])
            answer_content.append([])
            for j in range(outer_row_count):
                content[i].append([])
                answer_content[i].append([])
                for k in range(outer_col_count):
                    arr = utils.long_div.create_long_div_problem(args)
                    content[i][j].append(arr[0])
                    answer_content[i][j].append(arr[1])
    rendered_worksheet = template.render(col_spec=col_spec, content=content, title=TITLES[args.worksheet])
    rendered_answersheet = template.render(col_spec=col_spec, content=answer_content, title=TITLES[args.worksheet])
    return [rendered_worksheet, rendered_answersheet]
