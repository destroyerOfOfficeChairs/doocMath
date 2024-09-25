import datetime
import os
import random
import subprocess
import sys
from jinja2 import Template

import utils.handle_args
import utils.latex
import utils.long_div
import utils.vertical_problem

def generate_output_directory(worksheet):
    # Create a timestamped directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{timestamp}_{worksheet}"
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
    args = utils.handle_args.handle_args()
    rendered_worksheet = utils.latex.render_worksheet(args)
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
