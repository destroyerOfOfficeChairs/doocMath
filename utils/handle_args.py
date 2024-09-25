import argparse
import textwrap

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
        choices=["add", "sub", "addsub", "mult", "long-div", "borrow", "carry-over"],
        help=textwrap.dedent("""\
    The type of worksheet you would like to create. Supported types are:
    add - contains addition problems
    sub - contains subtraction problems
    addsub - contains addition and subtraction problems
    mult - contains multiplication problems
    long-div - contains long division problems
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
    B / A
    
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
    B / A
    
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

    # THIS WILL BE A FEATURE IN THE NEAR FUTURE
    #
    # parser.add_argument(
    #     "--r0",
    #     action="store_true",
    #     help=textwrap.dedent("""\
    #     Boolean flag. If set, then all quotients will have no remainder.""")
    # )

    args = parser.parse_args()

    if ((args.digits > 0 and (args.digits_A > 0 or args.digits_B > 0)) or
        (args.digits == 0 and args.digits_A == 0 and args.digits_B == 0)):
        parser.error("""Use EITHER --digits OR BOTH --digits-in-operand-A AND --digits-in-operand-B""")

    return args
