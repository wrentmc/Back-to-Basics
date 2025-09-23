import warnings
import os
import sys
import tabulate
from typing import Any, Callable
import math
import random
import re

class StackUnderflow(Exception):
    pass
class LoopError(Exception):
    pass
class LoopWarning(UserWarning):
    pass
class NameError(Exception):
    pass
class MathError(Exception):
    pass
class EndError(Exception):
    pass

stack = []
pointer = 0
end = 0
loops = []
ifs = 0
PRINT = print
NUM = float


def chs(n:NUM=2):
    if len(stack) < n:
        raise StackUnderflow("Not enough stack values to execute function")

def PUSH(n: NUM):
    stack.append(n)

def POP():
    chs(1)
    return stack.pop()

def ADD():
    chs()
    PUSH(POP()+POP())

def SUB():
    chs()
    PUSH(POP()-POP())

def BURY():
    chs()
    n = POP()
    v = POP()
    chs(n)
    stack.insert(-n,v)

def NIN():
    inp = input()
    PUSH(NUM(inp))

def CIN():
    PUSH(ord(input()))

def OUTN():
    PRINT(NUM(POP()))

def OUTC():
    a=chr(POP())
    PRINT(a, end="")

def SLOOP():
    global pointer
    global end
    global loops
    chs(1)
    amount = POP()
    loops.append([pointer+1, amount-1])

def ELOOP():
    global pointer
    global end
    global loops
    if len(loops) == 0:
        raise LoopError("Attempted to close a nonexistent loop. This is most likely caused by an ELOOP with no corresponding SLOOP.")
    if loops[-1][1] <= 0:
        loops.pop()
    else:
        pointer = loops[-1][0]-1
        loops[-1][1]-=1

def PASS():
    pass

def ZRO():
    PUSH(0)

def INC():
    PUSH(POP()+1)

def DEC():
    PUSH(POP()-1)

def DUP():
    PUSH(stack[-1])

def MUL():
    PUSH(POP()*POP())

def DIV():
    PUSH(POP()/POP())

def SIN():
    PUSH(math.sin(POP()))

def COS():
    PUSH(math.cos(POP()))

def TAN():
    PUSH(math.tan(POP()))

def ARCSIN():
    a = POP()
    if (a < -1 or a > 1):
        raise MathError("Arcsin parameters must be in between -1 and 1.")
    PUSH(math.asin(a))

def ARCCOS():
    a = POP()
    if (a < -1 or a > 1):
        raise MathError("Arccos parameters must be in between -1 and 1.")
    PUSH(math.acos(a))

def ARCTAN():
    PUSH(math.atan(POP()))

def EXP():
    chs()
    PUSH(POP()**POP())

def LOG():
    PUSH(math.log(POP()))

def LOGBASE():
    chs()
    PUSH(math.log(POP(),POP()))

def RND():
    PUSH(random.random())

def INT():
    PUSH(NUM(int(POP())))

def AND():
    chs()
    PUSH(POP() & POP())

def OR():
    chs()
    PUSH(POP() | POP())

def XOR():
    chs()
    PUSH(POP() ^ POP())

def NOT():
    PUSH(~POP())

def LSHIFT():
    chs()
    PUSH(POP()<<POP())

def RSHIFT():
    chs()
    PUSH(POP()>>POP())

def IFEQ():
    global ifs
    chs()
    if POP() != POP():
        ifs += 1

def IFNEQ():
    global ifs
    chs()
    if POP() == POP():
        ifs += 1

def IFGT():
    global ifs
    chs()
    if POP() <= POP():
        ifs += 1

def IFLS():
    global ifs
    chs()
    if POP() >= POP():
        ifs += 1

def END():
    global ifs
    if ifs > 0:
        ifs -=1
    else:
        raise SyntaxError("Attempted to END nonexistant statement.")

def CMT():
    pass

def READ(code, title=True):
    global pointer
    global end
    global loops
    global ifs
    if code.count("-") != 2:
        raise SyntaxError("Code must contain a single starting point and a single ending point, both notated by a '-'.")
    if title:
        if ("NAME " in code) and (code[code.index("NAME "):].count("-") == 2):
            if code.count("NAME") > 1:
                raise NameError("Only one NAME statement is allowed.")
            nmsg = (code[code.index("NAME "):code[code.index("NAME "):].replace('\\.', 'PD').index('.')].replace('\n',' '))[5:].replace('\\.', '.')
            code = code[code.index('N')+1+len(nmsg.replace('.','\\.')):]
            PRINT(f"RUNNING: {nmsg}")
        else:
            PRINT(f"RUNNING: <untitled>")
    if code.count("-") != 2:
        raise SyntaxError("Code must contain a single starting point and a single ending point, both notated by a '-'.")
    code = code[code.index('-')+1:]
    code = code[:code.index('-')]
    code = re.sub(r'\.[ ]+','.\n',code)
    code = code.replace('\n','').split('.')
    for i in code:
        if i not in l.keys():
            if str(i).split(" ")[0] != "CMT":
                raise SyntaxError(f"{i} is not a recognized function. Ensure line endings are present.")
    pointer = 0
    end = len(code)-1
    while pointer <= end:
        if code[pointer].split(" ")[0] == "CMT":
            pointer += 1
            continue
        if ifs == 0:
            l[code[pointer]]()
        elif l[code[pointer]] == END:
            l[code[pointer]]()
        pointer+=1
    if len(loops) > 0:
        warnings.warn("Unclosed SLOOP detected. Code completed successfully, but could be erroneous.", LoopWarning)

cmds = [i.split(': ') for i in """\
ADD: Math: Pop the first two values off the stack and add them. Push the result to the stack.
SUB: Math: Subtract the first value of the stack by the second value. Push the result to the stack.
MUL: Math: Multiply the top two stack values and push the result to the stack.
DIV: Math: Divide the top stack value by the second stack value. Push the result to the stack.
INC: Math: Increment the top stack value by one.
DEC: Math: Decrement the top stack value by one.
SIN: Math: Take the sine value of the first stack value and update it on the stack.
COS: Math: Take the cosine value of the first stack value and update it on the stack.
TAN: Math: Take the tangent value of the first stack value and update it on the stack.
ARCSIN: Math: Take the arcsine value of the first stack value and update it on the stack.
ARCCOS: Math: Take the arccosine value of the first stack value and update it on the stack.
ARCTAN: Math: Take the arctangent value of the first stack value and update it on the stack.
EXP: Math: Pop the first value off the stack and take it to the power of the second popped value.
LOG: Math: Take the natural logarithm (base e) of the first stack value.
LOGBASE: Math: Take the logarithm of the first stack value to the base of the second value.
RND: Math: Push a random value between 0 and 1 (inclusive) to the stack.
INT: Math: Truncate the first stack value to the integer part. (Stays in NUM type.)
AND: Math: Perform bitwise AND on the top two stack values.
OR: Math: Perform bitwise OR on the top two stack values.
XOR: Math: Perform bitwise XOR on the top two stack values.
NOT: Math: Perform bitwise NOT on the top stack value. Due to the usage of floating bits, this is the number gained from switching 1s and 0s.
AND: Math: Perform bitwise AND on the top two stack values.
LSHIFT: Math: Pushes the top stack value shifted to the left by the second value.
RSHIFT: Math: Pushes the top stack value shifted to the right by the second value.
POP: Stack: Pop the first value off the stack. Intended for internal use but still technically callable.
BURY: Stack: Bury the second value in the stack by the first value.
ZRO: Stack: Push a zero value to the stack.
DUP: Stack: Duplicate the top stack value.
NIN: I/O: Take numerical user input and push it to the stack.
CIN: I/O: Take user input, convert it to unicode, and push it to the stack.
OUTN: I/O: Pop the first value off the stack and output it as NUM.
OUTC: I/O: Pop the first value off the stack and output it as STR.
SLOOP: Conditional/Loop: Basic loop. Value popped is the number of times to loop between SLOOP and ELOOP.
ELOOP: Conditional/Loop: Mark an endpoint of a loop.
IFEQ: Conditional/Loop: If the top two (popped) stack values are equal, execute commands until END is executed.
IFNEQ: Conditional/Loop: If the top two (popped) stack values are not equal, execute commands until END is executed.
IFGT: Conditional/Loop: If the top stack value is greater than the second stack value, execute commands until END is executed.
IFLS: Conditional/Loop: If the top stack value is less than the second stack value, execute commands until END is executed.
END: Conditional/Loop: Mark the end of a conditional statement.
NAME: Other: Set the name of the program. Executed before the starting point. (e.g. NAME hello world\\. :).)
PASS: Other: Do nothing. For internal use, though technically callable.
CMT: Other: Specify that what follows is a comment (must be closed by a period, escaping not supported).""".split('\n')]
hmsg = """
╭─────────────────────╮
│Back To Basics v1.0.0│
╰─────────────────────╯
This is a language developed to simulate early programming.
--
Almost all commands have zero arguments and instead use stack values. For a list of commands, pass in the "--commands" flag.
Each program has a starting point and an ending point, both notated by a hyphen: -
Almost all commands must be contained within the starting and ending points to be executed.
The NAME command, however, comes before the starting point.
--
There are two main data types: NUM and STR.
NUMs are floating-point and are therefore not limited to integers.
for trigonometric functions, inputs are assumed to be in radians.
--
OUTN will print a line break automatically, but OUTC will only print what it is given.
--
See below for a sample program:
╭────────────────────────────────╮
│NAME I wonder what 4+4 is\\.\\.\\..│
│-                               │
│ZRO.                            │
│INC.                            │
│INC.                            │
│DUP.                            │
│MUL.                            │
│DUP.                            │
│MUL.                            │
│DUP.                            │
│ZRO.                            │
│INC.                            │
│INC.                            │
│DUP.                            │
│DEC.                            │
│BURY.                           │
│DIV.                            │
│OUTN.                           │
│-                               │
╰────────────────────────────────╯

Flags:
-h (--help)      show this message
-c (--commands)  show command list
-n (--notitle)   do not show title
"""
l: dict[str, Callable[..., Any]] = {'':PASS}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__ and key not in ["READ", "chs", "PUSH"]:
        l[key] = value
try:
    if sys.argv[1] in ['--commands', '-c']:
        PRINT(tabulate.tabulate(cmds,headers=['Command', 'Type', 'Description'], tablefmt='rounded_grid'))
    elif sys.argv[1] in ['--help', '-h']:
        PRINT(hmsg)
    else:
        try:
            if sys.argv[2] in ['--notitle', '-n']:
                with open(sys.argv[1]) as file:
                    READ(file.read(), title=False)
            else:
                PRINT(f"Unrecognized flag '{sys.argv[2]}'")
        except IndexError:
            with open(sys.argv[1]) as file:
                READ(file.read())
except IndexError:
    PRINT("Specify a file to run or specify a flag. (Hint: use the '-h' flag)")
except FileNotFoundError:
    PRINT(f"File or parameter {sys.argv[1]} not found")