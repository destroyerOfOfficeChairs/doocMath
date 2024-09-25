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
        content = [[[utils.vertical_problem.create_vertical_problem(args) for i in range(outer_col_count)] for j in range(outer_row_count)] for k in range(args.pages)]
    else:
        content = [[[utils.long_div.create_long_div_problem(args) for i in range(outer_col_count)] for j in range(outer_row_count)] for k in range(args.pages)]
    rendered_worksheet = template.render(col_spec=col_spec, content=content, title=TITLES[args.worksheet])
    return rendered_worksheet
