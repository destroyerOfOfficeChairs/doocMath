import utils.operands

from jinja2 import Template

def create_long_div_problem(args):
    operands = utils.operands.create_two_operands(args)
    a = operands[0]
    b = operands[1]
    quotient = round(b / a, 3)
    with open("templates/long_division.j2") as file:
        template = Template(file.read(), variable_start_string="<<", variable_end_string=">>")
    rendered_problem = template.render(divisor=a, dividend=b, quotient = " ")
    rendered_answer = template.render(divisor=a, dividend=b, quotient=quotient)
    return [rendered_problem, rendered_answer]
