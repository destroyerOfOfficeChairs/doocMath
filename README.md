# doocMath

This project is dedicated to my homeschooled daughter, whom I love so much.

doocMath is a command-line tool designed to create customizable arithmetic
worksheets in PDF format. Whether you're a teacher, a homeschooling parent, or
someone looking to practice math skills, doocMath offers a quick and easy way
to generate math problems tailored to your needs.

### Version

1.6.0

## Features

- Create unique math worksheets with addition, subtraction, addition AND
subtraction, multiplication, and long division problems.
- Answer key is generated along with worksheets.
- Create a special kind of subtraction worksheet, the `borrow` worksheet, where
every problem requires borrowing to answer correctly.
- Create a special kind of addition worksheet, the `carry-over` worksheet,
where every problem requires carrying-over to answer correctly.
- Generate the kind of worksheet you need with command line arguments.
- run `python3 doocMath.py --help` to see everything you need to know.
- Specify the number of digits for each operand.
- In subtraction problems, the minuend will always be greater than or equal to
the subtrahend -- meaning the difference will always be greater than or equal
to 0.
- Generate multi-page PDFs.
- Currently, all worksheet problems are in the vertical format, except for long
division problems.

## Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/destroyerOfOfficeChairs/doocMath.git
   cd doocMath
   ```

2. **Install Minimal LaTeX (Linux/Ubuntu):**
   
   Since the only package doocMath requires is the `geometry` package, install
   `texlive-latex-base`:
   
   ```
   sudo apt install texlive-latex-base
   ```

   This gives you a minimal LaTeX setup that allows you to use doocMath
   efficiently without taking up too much space on your system.

3. **Install Python Packages**

   Jinja2 is the only required Python package. doocMath uses Jinja2 to create
   LaTeX documents.

   ```
   pip install jinja2
   ```
   
## Types Of Worksheets

One of the arguments doocMath requires is `--worksheet`

Currently, there are 7 kinds of supported worksheets:

1. `add` [A + B] Addition problems
2. `sub` [A - B] Subtraction problems
3. `addsub` [A + B] or [A - B] Addition AND subtraction problems
4. `mult` [A * B] Multiplication problems
5. `long-div` [B / A] Long division problems
5. `borrow` [A - B] Subtraction problems that all require borrowing
6. `carry-over` [A + B] Addition problems that all require carrying-over
   
## Usage

There are only a few arguments doocPress requires you to use, whereas the rest
are optional. You must use the `--worksheet` argument and the `--digits`
argument.

`--worksheet` specifies the type of worksheet you would like to create.

`--digits` specifies the max number of digits each operand should be capable of
having.

Once you run doocMath, a directory is created within the repo directory which
contains your custom and unique worksheet.

ALTERNATELY:

You could specify `--digits_A` and `--digits_B` to have finer control of how
many digits each operand should be capable of having.

EXAMPLES:

Generate a single-page worksheet with addition and subtraction problems with
operands between 1-99:

```
python3 doocMath.py --worksheet addsub --digits 2
```

Generate 20 worksheets with addition and subtraction problems with operands
between 1-99:

```
python3 doocMath.py --worksheet addsub --digits 2 --pages 20
```

Generate 10 worksheets with subtraction problems with the minuend having 3
digits and the subtrahend having 2 digis:

```
python3 doocMath.py --worksheet sub --digits_A 3 --digits_B 2 --pages 10
```

## Roadmap

Here are a few ways doocMath could be improved in the future:

- Customizable operand ranges
- Flag to generate long division problems where the quotient is always an
integer
- Fractions worksheets
- Decimal operations

## Contributing

Contributions are welcome! Please fork the repository and submit a pull
request. Before contributing, please ensure that you have tested your changes
thoroughly.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### 1.6.0

- Answer keys are now automatically generated along with worksheets.

### 1.5.0

- Refactored the codebase. Now it should be easier to read, maintain, and add new features.
- Newly created directories now begin with the timestamp instead of the worksheet type.

### 1.4.0

- Added `long-div` worksheet, which contains long division problems.

### 1.3.0

- Added the ability to create the `carry-over` addition worksheet. Every
problem requires carrying-over to answer correctly.

### 1.2.0

- Added Titles to each worksheet. Titles correspond to the type of worksheet
generated.

### 1.1.0

- Added the ability to create the `borrow` subtraction worksheet. Every problem
requires borrowing to answer correctly.

### 1.0.1

- Removed unused packages.
- Changed instructions in README.md

### 1.0

- Initial commit
